export PYTHONPATH=/workspace/GithubRepo/pr-agent_dev
export LOGLEVEL=DEBUG
# python3.9 pr_agent/cli.py --pr_url https://github.com/XieYunshen/gitskills/pull/1 review
python3.9 pr_agent/cli.py --pr_url https://github.com/XieYunshen/gitskills/pull/1 describe
# python3.9 pr_agent/cli.py --pr_url https://github.com/PaddlePaddle/Paddle/pull/58094 describe
# python3.9 pr_agent/cli_v1.py
# python3.9 main.py
