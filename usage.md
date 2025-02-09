

```
virtualenv -p /usr/bin/python venv-harness
. venv-harness/bin/activate 

cd /shared/chuan
git clone https://github.com/LambdaLabsML/lm-evaluation-harness
cd lm-evaluation-harness
git checkout lambda
pip install -e ".[math,ifeval,sentencepiece]"
pip install vllm==0.7.2
pip install tabulate

huggingface-cli login

./run_bash.sh deepseek8b 8
```