FROM inseefrlab/onyxia-python-minimal

COPY app ./
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["flask", "--app", "main", "run", "--host", "0.0.0.0", "-p", "5000"]
