FROM inseefrlab/onyxia-python-minimal

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
#EXPOSE 5000
EXPOSE 3838
ENTRYPOINT ["flask", "--app", "main", "run", "--host", "0.0.0.0", "-p", "3838"]
