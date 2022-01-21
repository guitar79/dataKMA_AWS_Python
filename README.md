# dataKMA_Python

가상환경 리스트 보기
> conda env list

#windows
##가상환경 생성하기 (windows)
conda create -n dataKMA_AWS_Python_wiu_env

##가상환경 시작하기 (windows)
conda activate dataKMA_AWS_Python_win_env

##install module
conda install selenium spyder

##가상환경 내보내기 (windows)
conda env export > dataKMA_AWS_Python_win_env.yaml

##.yaml 파일로 새로운 가상환경 만들기  (windows)
conda env create -f dataKMA_AWS_Python_win_env.yaml

##deactivate 가상환경 종료
conda deactivate

##가상환경 제거하기 (windows)
conda env remove -n dataKMA_AWS_Python_win_env


#ubuntu

##가상환경 생성하기 (ubuntu)
conda create -n dataKMA_AWS_Python_ubuntu_env

##가상환경 시작하기 (ubuntu)
conda activate dataKMA_AWS_Python_ubuntu_env

##install module
conda install selenium spyder

##가상환경 내보내기 (ubuntu)
conda env export > dataKMA_AWS_Python_ubuntu_env.yaml

##.yaml 파일로 새로운 가상환경 만들기 (ubuntu)
conda env create -f dataKMA_AWS_Python_ubuntu_env.yaml

##deactivate 가상환경 종료
conda deactivate

##가상환경 제거하기(ubuntu)
conda env remove -n dataKMA_AWS_Python_ubuntu_env
