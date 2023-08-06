// -*- tab-width: 8; indent-tabs-mode: nil; c-basic-offset: 4 -*-
// vi: set et ts=8 sw=4 sts=4:

//File that uses the tnnmg module instead of dune-fufem

#include <config.h>

#include <array>
#include <iostream>
#include <sstream>

// dune-common includes
#include <dune/common/bitsetvector.hh>
#include <dune/common/parallel/mpihelper.hh>
#include <dune/common/stringutility.hh>
#include <dune/common/test/testsuite.hh>

// dune-istl includes
#include <dune/istl/bcrsmatrix.hh>

// dune-grid includes
#include <dune/grid/yaspgrid.hh>
#include <dune/grid/io/file/vtk/vtkwriter.hh>

// dune-solver includes
#include <dune/solvers/common/defaultbitvector.hh>
#include <dune/solvers/iterationsteps/obstacletnnmgstep.hh>
#include <dune/solvers/iterationsteps/multigridstep.hh>
#include <dune/solvers/iterationsteps/truncatedblockgsstep.hh>
#include <dune/solvers/norms/energynorm.hh>
#include <dune/solvers/solvers/loopsolver.hh>
// #include <dune/solvers/test/common.hh>
#include <dune/solvers/transferoperators/compressedmultigridtransfer.hh>


//dune-fufem includes
#include <dune/fufem/assemblers/transferoperatorassembler.hh>
#include <dune/fufem/utilities/gridconstruction.hh>

// dune-tnnmg includes
#include <dune/tnnmg/functionals/quadraticfunctional.hh>
#include <dune/tnnmg/functionals/boxconstrainedquadraticfunctional.hh>
#include <dune/tnnmg/functionals/bcqfconstrainedlinearization.hh>
#include <dune/tnnmg/iterationsteps/nonlineargsstep.hh>
#include <dune/tnnmg/iterationsteps/tnnmgstep.hh>

#include <dune/tnnmg/localsolvers/scalarobstaclesolver.hh>

#include <dune/tnnmg/projections/obstacledefectprojection.hh>

// #include <dune/solvers/test/common.hh>


template <class DomainType, class RangeType, class F>
class FunctionFromLambda :
    public Dune::VirtualFunction<DomainType, RangeType>
{
    public:
        FunctionFromLambda(F f):
            f_(f)
    {}

        void evaluate(const DomainType& x, RangeType& y) const
        {
            y = f_(x);
        }

    private:
        F f_;
};

template<class Domain, class Range, class F>
auto makeFunction(F&& f)
{
    return FunctionFromLambda<Domain, Range, std::decay_t<F>>(std::forward<F>(f));
}


//stripped down version of solving obstacle problem by truncated non-smooth newton multi-grid method
template<class GridViewType, class MatrixType, class VectorType>
void solveObstacleProblemByTNNMG(const GridViewType& gridview, const MatrixType& mat, VectorType& x, const VectorType& rhs, const  VectorType& lower_, const int upper_, int maxIterations=100, double tolerance=1.0e-10)
{

    //todo
    //do all the marking of the boudary DOF inside here at the moment, eventually export into python
    typedef typename ObstacleTNNMGStep<MatrixType, VectorType>::BitVector BitVector;
    BitVector ignore(rhs.size());
    ignore.unsetAll();


    typedef VectorType Vector;
    typedef MatrixType Matrix;
    typedef EnergyNorm<Matrix, Vector> Norm;
    typedef ::LoopSolver<Vector> Solver;
    typedef ObstacleTNNMGStep<Matrix, Vector> TNNMGStep;
    typedef typename TNNMGStep::Transfer Transfer;
    typedef typename TNNMGStep::BoxConstraintVector BoxConstraintVector;
    typedef CompressedMultigridTransfer<Vector, BitVector, Matrix> TransferImplementation;

    const int blockSize = VectorType::block_type::dimension;

    //assemble hierarchy of matricies all at once
    using TOA = TransferOperatorAssembler<GridViewType>;
    std::vector<std::shared_ptr<Matrix>> transfer_mat;
    TOA toa(gridview);
    toa.assembleMatrixHierarchy(transfer_mat);

    //needs to be gridview.hierarchicalGrid.maxLevel()
    std::vector<std::shared_ptr<Transfer>> transfer(gridview.grid().maxLevel());

    //now put this matrix hierarchy into a hierarchy of Transfer objects
    for (size_t i = 0; i < transfer.size(); i ++)
    {
        auto t = std::make_shared<TransferImplementation>(transfer_mat[i]);
        transfer[i] = t;
    }

    auto lower = Vector(rhs.size());
    auto upper = Vector(rhs.size());

    lower = lower_;
    upper = upper_;

    //lower = -1;
    //upper = +1;

    //lower = 0;
    //upper = 1;


    using Functional = Dune::TNNMG::BoxConstrainedQuadraticFunctional<Matrix&, Vector&, Vector&, Vector&, double>;
    auto J = Functional(mat, rhs, lower, upper);

    auto localSolver = gaussSeidelLocalSolver(Dune::TNNMG::ScalarObstacleSolver());

    using NonlinearSmoother = Dune::TNNMG::NonlinearGSStep<Functional, decltype(localSolver), BitVector>;
    auto nonlinearSmoother = std::make_shared<NonlinearSmoother>(J, x, localSolver);

    auto smoother = TruncatedBlockGSStep<Matrix, Vector>{};

    auto linearMultigridStep = std::make_shared<Dune::Solvers::MultigridStep<Matrix, Vector> >();
    linearMultigridStep->setMGType(1, 3, 3);
    linearMultigridStep->setSmoother(&smoother);
    linearMultigridStep->setTransferOperators(transfer);

    using Linearization = Dune::TNNMG::BoxConstrainedQuadraticFunctionalConstrainedLinearization<Functional, BitVector>;
    using DefectProjection = Dune::TNNMG::ObstacleDefectProjection;
    using LineSearchSolver = Dune::TNNMG::ScalarObstacleSolver;
    using Step = Dune::TNNMG::TNNMGStep<Functional, BitVector, Linearization, DefectProjection, LineSearchSolver>;

    using Solver = LoopSolver<Vector>;
    using Norm =  EnergyNorm<Matrix, Vector>;


    using Step = Dune::TNNMG::TNNMGStep<Functional, BitVector, Linearization, DefectProjection, LineSearchSolver>;
    int mu=1; // #multigrid steps in Newton step
    auto step = Step(J, x, nonlinearSmoother, linearMultigridStep, mu, DefectProjection(), LineSearchSolver());

    auto norm = Norm(mat);
    auto solver = Solver(step, 1e9, 0, norm, Solver::FULL);

    step.setIgnore(ignore);
    step.setPreSmoothingSteps(3);

    solver.addCriterion(
            [&](){
            return Dune::formatString("   % 12.5e", J(x));
            },
            "   energy      ");

    double initialEnergy = J(x);
    solver.addCriterion(
            [&](){
            static double oldEnergy=initialEnergy;
            double currentEnergy = J(x);
            double decrease = currentEnergy - oldEnergy;
            oldEnergy = currentEnergy;
            return Dune::formatString("   % 12.5e", decrease);
            },
            "   decrease    ");

    solver.addCriterion(
            [&](){
            return Dune::formatString("   % 12.5e", step.lastDampingFactor());
            },
            "   damping     ");


    solver.addCriterion(
            [&](){
            return Dune::formatString("   % 12d", step.linearization().truncated().count());
            },
            "   truncated   ");


    std::vector<double> correctionNorms;
    solver.addCriterion(Dune::Solvers::correctionNormCriterion(step, norm, 1e-10, correctionNorms));

    solver.preprocess();
    solver.solve();
    std::cout << correctionNorms.size() << std::endl;
}
