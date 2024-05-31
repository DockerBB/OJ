import time

from flask import Flask, request, jsonify
import os
import subprocess
import tempfile
import shutil

app = Flask(__name__)

TESTCASE_DIR = '/app/judge_service/testcase'
TEMP_DIR = '/app/judge_service/tmp/'

@app.route('/problems/<int:pid>/judge', methods=['POST'])
def judge(pid):
    data = request.get_json()
    language = data['language']
    code = data['code']
    test_input_dir = os.path.join(TESTCASE_DIR, str(pid), 'inputs')
    test_output_dir = os.path.join(TESTCASE_DIR, str(pid), 'outputs')

    # 读取测试输入和输出文件
    test_inputs = []
    test_outputs = []
    for filename in os.listdir(test_input_dir):
        with open(os.path.join(test_input_dir, filename), 'r') as f:
            test_inputs.append(f.read().strip())
    for filename in os.listdir(test_output_dir):
        with open(os.path.join(test_output_dir, filename), 'r') as f:
            test_outputs.append(f.read().strip())

    # 使用提供的代码和测试文件进行验证
    results = []
    passed_count = 0
    for test_input, test_output in zip(test_inputs, test_outputs):
        result = run_test(language, code, test_input, test_output)
        results.append(result)
        if result['status'] == 'passed':
            passed_count += 1

    # 根据测试结果返回状态
    total_tests = len(test_inputs)
    if passed_count == total_tests:
        return jsonify({'status': 'pass'})
    else:
        return jsonify({'status': 'error', 'message': f'{passed_count}/{total_tests} tests passed'})

@app.route('/problems/<int:pid>/test_cases', methods=['GET', 'POST'])
def test_cases(pid):
    if request.method == 'GET':
        # 返回指定问题 ID 的测试用例
        input_file = os.path.join(TESTCASE_DIR, str(pid), 'inputs', 'input.txt')
        output_file = os.path.join(TESTCASE_DIR, str(pid), 'outputs','output.txt')
        with open(input_file, 'r') as f:
            test_inputs = [line.strip() for line in f.readlines()]
        with open(output_file, 'r') as f:
            test_outputs = [line.strip() for line in f.readlines()]
        return jsonify({'test_inputs': test_inputs, 'test_outputs': test_outputs})
    elif request.method == 'POST':
        # 更新指定问题 ID 的测试用例
        data = request.get_json()
        test_inputs = data['test_inputs']
        test_outputs = data['test_outputs']
        sign = int(time.time())
        intput_txt = f'input_{sign}.txt'
        output_txt = f'output_{sign}.txt'
        # 创建目录并保存测试用例
        os.makedirs(os.path.join(TESTCASE_DIR, str(pid), 'inputs'), exist_ok=True)
        os.makedirs(os.path.join(TESTCASE_DIR, str(pid), 'outputs'), exist_ok=True)
        input_file = os.path.join(TESTCASE_DIR, str(pid), 'inputs', intput_txt)
        output_file = os.path.join(TESTCASE_DIR, str(pid), 'outputs', output_txt)
        with open(input_file, 'w') as f:
            f.write('\n'.join(test_inputs))
        with open(output_file, 'w') as f:
            f.write('\n'.join(test_outputs))
        return jsonify({'message': 'Test cases updated successfully'})

def run_test(language, code, test_input, test_output):
    # 实现测试代码的运行逻辑
    if language == 'python':
        return run_python_test(code, test_input, test_output)
    elif language == 'cpp':
        return run_cpp_test(code, test_input, test_output)
    elif language == 'java':
        return run_java_test(code, test_input, test_output)
    else:
        return {'status': 'error', 'message': 'Unsupported language'}


def run_python_test(code, test_input, test_output):
    # 创建临时目录
    os.makedirs(TEMP_DIR, exist_ok=True)

    # 创建临时文件
    temp_file_path = os.path.join(TEMP_DIR, 'temp_file.py')
    with open(temp_file_path, 'w') as f:
        f.write(code)

    # 创建输入文件
    input_file_path = os.path.join(TEMP_DIR, 'input.txt')
    with open(input_file_path, 'w') as f:
        f.write(test_input)

    try:
        # 从输入文件读取内容,并将其作为字符串传递给 subprocess.run()
        with open(input_file_path, 'r') as f:
            input_data = f.read()
        result = subprocess.run(['python', temp_file_path], check=True, input=input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # 检查脚本是否成功执行
        if result.returncode == 0:
            actual_output = result.stdout.strip()
            print(actual_output)
            if actual_output == test_output:
                return {'status': 'passed'}
            else:
                return {'status': 'failed', 'expected': test_output, 'actual': actual_output}
        else:
            return {'status': 'error', 'message': result.stderr}
    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': e.stderr}
    finally:
        os.remove(temp_file_path)
        os.remove(input_file_path)

def run_cpp_test(code, test_input, test_output):
    # 创建临时目录
    os.makedirs(TEMP_DIR, exist_ok=True)

    # 创建临时 C++ 文件
    temp_file_path = os.path.join(TEMP_DIR, 'temp_file.cpp')
    with open(temp_file_path, 'w') as f:
        f.write(code)

    # 创建输入文件
    input_file_path = os.path.join(TEMP_DIR, 'input.txt')
    with open(input_file_path, 'w') as f:
        f.write(test_input)

    try:
        # 从输入文件读取内容,并将其作为字符串传递给 subprocess.run()
        with open(input_file_path, 'r') as f:
            input_data = f.read()
        result = subprocess.run(['g++', '-std=c++11', '-o', 'temp_file', temp_file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result = subprocess.run(['./temp_file'], check=True, input=input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # 检查程序是否成功执行
        if result.returncode == 0:
            actual_output = result.stdout.strip()
            print(actual_output)
            if actual_output == test_output:
                return {'status': 'passed'}
            else:
                return {'status': 'failed', 'expected': test_output, 'actual': actual_output}
        else:
            return {'status': 'error', 'message': result.stderr}
    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': e.stderr}
    finally:
        os.remove(temp_file_path)
        os.remove(input_file_path)

def run_java_test(code, test_input, test_output):
    # 创建临时目录
    os.makedirs(TEMP_DIR, exist_ok=True)

    # 创建临时 Java 文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=TEMP_DIR, suffix='.java') as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(code)

    # 创建输入文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=TEMP_DIR, suffix='.txt') as input_file:
        input_file_path = input_file.name
        input_file.write(test_input)

    try:
        # 编译 Java 代码
        print('Compiling Java code...')
        compile_result = subprocess.run(['javac', temp_file_path], check=True, stderr=subprocess.PIPE, universal_newlines=True)

        # 运行 Java 程序
        print('Running Java program...')
        run_result = subprocess.run(['java', '-classpath', TEMP_DIR, 'Solution'],
                                   check=True,
                                   input=test_input,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)

        # 读取程序输出
        actual_output = run_result.stdout.strip()
        print('Actual output:', actual_output)

        # 比较输出
        if actual_output == test_output:
            return {'status': 'passed'}
        else:
            return {'status': 'failed', 'expected': test_output, 'actual': actual_output}

    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': e.stderr}

    finally:
        os.remove(temp_file_path)
        os.remove(input_file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9900)