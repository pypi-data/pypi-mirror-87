git clone https://gitlab.dune-project.org/staging/dune-typetree
git clone https://gitlab.dune-project.org/staging/dune-functions
git clone https://git.imp.fu-berlin.de/agnumpde/dune-matrix-vector.git
git clone https://git.imp.fu-berlin.de/agnumpde/dune-fufem.git
git clone https://git.imp.fu-berlin.de/agnumpde/dune-solvers.git
git clone https://git.imp.fu-berlin.de/agnumpde/dune-tnnmg.git

cd dune-fufem
git checkout 1d36a4c802aa2fe588c09225e584c4a11494e938
git apply ../patches/dune-fufem*.diff
cd ..

install_prefix=$1

build() {
mkdir build
cd build
cmake .. -G Ninja -DCMAKE_INSTALL_PREFIX:PATH=$install_prefix
  -DSKBUILD:BOOL=TRUE\
  -DBUILD_SHARED_LIBS=TRUE\
  -DUSE_PTHREADS=ON\
  -DCMAKE_BUILD_TYPE=Release\
  -DCMAKE_DISABLE_FIND_PACKAGE_LATEX=TRUE\
  -DCMAKE_DISABLE_DOCUMENTATION=TRUE -DINKSCAPE=FALSE\
  -DCMAKE_INSTALL_RPATH=/home/dedner/DUNEPIPA/dune-env/lib/\
  -DCMAKE_MACOSX_RPATH=TRUE -DCMAKE_BUILD_TYPE:STRING=Release
ninja install
cd ..
}

cd dune-typetree
build
cd ../dune-functions
build
cd ../dune-matrix-vector
build
cd ../dune-solvers
build
cd ../dune-tnnmg
build
cd ../dune-fufem
build
cd ..
