FROM public.ecr.aws/lambda/python:3.11
COPY req.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r req.txt
COPY cosineSimilarity.py ${LAMBDA_TASK_ROOT}
CMD ["cosineSimilarity.handler"]