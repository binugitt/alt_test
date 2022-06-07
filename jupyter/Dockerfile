FROM bitnami/jupyter-base-notebook:2.3.0

RUN pip install matplotlib
RUN pip install pandas
RUN pip install pyzmq==22.3.0
RUN pip install zerorpc
RUN pip install mpl_finance
RUN pip install --upgrade mplfinance
RUN pip install plotly

#hostname: localhost
#CMD sudo chown $USER: ~/.local/share/jupyter

#CMD jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password=''
#CMD jupyter notebook --no-browser --ip='0.0.0.0' --NotebookApp.token='' --NotebookApp.password='' --allow-root --notebook-dir . -e JUPYTER_TOKEN=letmein
#CMD jupyter notebook --no-browser --ip='0.0.0.0' --NotebookApp.token='' --NotebookApp.password='' -e JUPYTER_TOKEN=letmein --allow-root --user root -w /home/binu/ -v $PWD/work:/home/binu

USER root
WORKDIR /home/binu/
CMD jupyter notebook --no-browser --ip='0.0.0.0' --NotebookApp.token='' --NotebookApp.password='' --allow-root
