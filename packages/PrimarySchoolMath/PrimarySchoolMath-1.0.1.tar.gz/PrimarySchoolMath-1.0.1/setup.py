import setuptools

# 读取项目的readme介绍
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PrimarySchoolMath",# 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    version="1.0.1",
    author="J.sky", # 项目作者
    author_email="bosichong@qq.com",
    description="小学生口算题的小应用", # 项目的一句话描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bosichong/PrimarySchoolMathematics",# 项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)