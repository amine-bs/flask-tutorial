FROM inseefrlab/onyxia-python-minimal

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["flask", "--app", "main", "run"]