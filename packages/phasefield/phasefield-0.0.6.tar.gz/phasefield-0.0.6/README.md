Automatic Construction of Phasefield Approximations from Sharp-Interface Models
===============================================================================

The title says it all: this module uses a simple description of a sharp
interface problem to derive a phasefield approximation which can then be
solved using a finite-element toolbox. The domain specific language
[UFL][ufllink] is used both for defining the sharp interface model and for
the weak formulation of the phasefield approximation. The resulting UFL form
can then be inserted into any of the finite element packages available
which can take UFL forms as an input. A class for evolving the solution
over time is available based on [dune][dunelink]  and [fenics][fenicslink].
The bindings for the `dune` package include both local grid refinement and
coarsening. This makes it easy to track the interface with a fine grid
while a coarser grid can be used away from the interface. This is essential
for evolving phasefield models efficiently. In addition the `dune` stepper
also provides an efficient solver for obstacle problems so that double
obstacle potentials can be used in the modelling. This solver is based
on [tnmg][tnmglink].

So far this module has been tested with:

- two phase models including additional bulk equations, e.g., for the temperature
- multphase models
- single phase models, e.g., crack propagation problems

Installation
------------
The easiest way to test this module is using the `docker` container provided.
Assuming `docker` is available on your system simply running the script
`rundune.sh` will download the docker image for the [dune-fem][fempylink]
package and start the container. Within the container running the
`phasefield.sh` script will complete the installation - this step takes
some time but is only required the first time the docker container is set
up. Within the docker container `/host` points to the folder from which
`rundune.sh` was started, e.g., the root folder of this repository.
Some examples are contained in the `tutorials` folder.
More information on using the docker container can be found
[here][fempylink] including some information for MAC and Windows user.

[ufllink]: https://fenics.readthedocs.io/projects/ufl/en/latest/
[fenicslink]: https://fenicsproject.org/
[dunepylink]: https://gitlab.dune-project.org/staging/dune-python
[dunelink]: http://dune-project.org
[fempylink]: https://gitlab.dune-project.org/dune-fem/dune-fem
[tnmglink]: https://
