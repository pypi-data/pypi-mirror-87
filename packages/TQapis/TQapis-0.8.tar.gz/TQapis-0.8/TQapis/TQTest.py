import os, pathlib
from .TQConnection import Connection, Message
from .TQRequests import ParamBuilder


def make_request( param, function_name):
    return ParamBuilder().build(param, function_name)


def delete_file(result_new_file_path):
    try:
        os.remove(result_new_file_path)
    except:
        pass
    return Message(True, "")


def write_test_file(file_path,section_tag, params, delimiter_char, comment_char):
    try:
        writefile = open(file_path, "w")
        for name, param in params:
            line = section_tag+":"+name+"\n"
            writefile.write(line)
            for key, value in param.items():
                line = key.lstrip()+ delimiter_char + value + "\n"
                writefile.write(line)
            writefile.write("\n")
        writefile.close()
        return Message(True, "")
    except Exception as e:
        return Message(False, str(e))


def read_test_file(file_path, section_tag, delimiter, comment):
    params = list()
    param = None
    try:
        line_cntr = 0
        inputfile = open(file_path, "r")
        for line in inputfile:
            # ignore blank lines
            if len(line.lstrip()) == 0:
                line_cntr += 1
                continue
            loc = line.rfind(comment)
            if loc == 0:
                line_cntr += 1
                continue

            #
            # a proper line to process
            #
            #has it got comment?
            if comment in line:
                line=line.split(comment)[0]
            #empty line on the ledt side?
            if line.rstrip().lstrip()=='':
                continue

            if section_tag in line:
                tag_name=""
                if ':' in line:
                    tag_name=line.split(':')[1].lstrip().rstrip().replace('\n','')
                param = dict()
                params.append((tag_name,param))
                continue

            if line.find(delimiter)==-1:
                line_cntr += 1
                return Message(False,
                               "Missing delimiter {} in file {} line:{}".format(delimiter, file_path,
                                                                                line_cntr)), params
            tokens = line.split(delimiter)
            tokens[0] = tokens[0].lstrip().rstrip()
            tokens[1] = tokens[1].lstrip().rstrip().replace('"', '')
            if len(tokens[0]) == 0:
                line_cntr += 1
                return Message(False,
                               "Missing delimiter key in key-value pair in file {} line:{}".format(file_path,
                                                                                                   line_cntr)), params
            if len(tokens[1]) == 0:
                line_cntr += 1
                return Message(False,
                               "Missing delimiter value in key-value pair in file {} line:{}".format(file_path,
                                                                                                     line_cntr)), params
            param[tokens[0]] = tokens[1]
            line_cntr += 1
        inputfile.close()
        return Message(True, ""), params
    except Exception as e:
        return Message(False, str(e)), params


class Runner:
    def __init__(self, email,is_post,target_url):
        self.__param_factory = [
            'describe'
            , 'account_password_change'
            , 'account_ip_change'
            , 'account_create'
            , 'account_send_activation_key'
            , 'account_activate'
            , 'market_fx_rates'
            , 'show_available'
            , 'workspace'
            , 'market_swap_rates'
            , 'pnl_attribute'
            , 'pnl_predict'
            , 'price'
            , 'price_fx_forward'
            , 'price_vanilla_swap'
            , 'risk_ladder'
        ]
        self.connection = Connection(email,is_post,target_url)

    def validate(self, params):
        if 'function_name' not in params:
            return Message(False, "There is no value for the key 'function_name'.")
        function_name = params['function_name']
        if function_name not in self.__param_factory:
            return Message(False, "function_name '" + function_name + "' is not recognised.")
        # param_builder = self.__param_factory[function_name]
        # message = param_builder.validate(params)
        # if not message.is_OK:
        #     return message
        return Message(True, "")

    def send(self, params):
        function_name = params['function_name']
        #param_builder = self.__param_factory[function_name]
        request = make_request(params, function_name)

        message = self.connection.send(request)
        return message

    def get_response(self):
        return self.connection.response

    def get_all_test_file_names(self, root_folder, request_extension):
        file_names = list()
        for root, dirs, files in os.walk(root_folder):
            for filename in files:
                fname, fextension = os.path.splitext(filename)
                if fextension.lower() == "." + request_extension.lower():
                    file_names.append(fname)
        return file_names

    def run(self, root_folder, request_extension='request', result_extension='result',
            result_new_extension='result_new'):
        report = dict()
        test_file_names = self.get_all_test_file_names(root_folder, request_extension)
        for test_file_name in test_file_names:
            message = self.execute_single_test(root_folder, test_file_name, request_extension, result_extension,
                                             result_new_extension)
            status_result = "OK"
            if len(message.content) > 0:
                status_result = message.content
            report[test_file_name] = status_result
            print ("{}:{}".format(test_file_name,status_result))
        return report

    def execute_single_test(self, root_folder, test_file_name, request_extension="request", result_extension="result", result_new_extension="result_new"):
        delimiter_char = '='
        comment_char = '#'
        test_section_tag = "[test]"
        result_section_tag = "[result]"

        request_file_path = os.path.join(root_folder, test_file_name + "." + request_extension)
        result_file_path = os.path.join(root_folder, test_file_name + "." + result_extension)
        result_new_file_path = os.path.join(root_folder, test_file_name + "." + result_new_extension)

        message, names_with_params = read_test_file(request_file_path,test_section_tag, delimiter_char, comment_char)

        result_news=list()
        if not message.is_OK:
            return message

        for name,param in names_with_params:
            message = self.validate(param)
            if not message.is_OK:
                return message

            message = self.send(param)
            return_values=dict()
            return_values= self.connection.response.results
            if not message.is_OK:
                return_values = self.connection.response.errors

            return_values_clean=dict()
            for key, value in  return_values.items():
                return_values_clean[key]=value.rstrip().lstrip()

            result_news.append((name,return_values_clean))
            message = delete_file(result_new_file_path)
            if not message.is_OK:
                return message



        message, base_results = read_test_file(result_file_path,result_section_tag, delimiter_char, comment_char)

        if (len(base_results) == 0):
            message = write_test_file(result_file_path,result_section_tag, result_news, delimiter_char, comment_char)
        elif base_results != result_news:
            message = write_test_file(result_new_file_path,result_section_tag, result_news, delimiter_char, comment_char)
            message.content = "New results generated!"
        return message


def run_test_all(folder, email, is_post, target_url="http://operations.treasuryquants.com"):
    # print(pathlib.Path(__file__).parent.absolute().joinpath("tests_files"))
    runner = Runner(email, is_post, target_url)
    return runner.run(folder)


def run_test_single(root_folder, file_path,email,is_post, target_url="http://operations.treasuryquants.com"):
    # print(pathlib.Path(__file__).parent.absolute().joinpath("tests_files"))
    runner = Runner(email,is_post, target_url)
    status_result = "OK"
    message=runner.execute_single_test(root_folder,file_path)
    if len(message.content) > 0:
        status_result = message.content
    print(file_path, status_result)
    report={file_path:status_result}
    return report


