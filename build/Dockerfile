FROM python:3.8.2-slim-buster
RUN mkdir -p /opt/module/rde
WORKDIR /opt/module/rde
COPY . ./
RUN python -m pip install --upgrade pip
RUN pip install pymysql web.py==0.61 pyjwt casbin requests -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8080
RUN nohup python ./tools/sync_policy.py > /dev/null 2>&1 &
CMD python run.py 8080