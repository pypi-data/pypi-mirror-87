#!/usr/bin/python

"""
this script is for UFES L7policy Validator automation build and get its artifacts
"""
import os
import sys
import argparse

from io import StringIO
from jenkinsapi.custom_exceptions import ArtifactBroken
from jenkinsapi.jenkins import Jenkins


class JenkinsApplication:
    def __init__(self, url, job_name, verbose=True):
        self.url = url
        self.job_name = job_name
        self.params = {}
        self.files = {}
        self.jenkins = None
        self.job = None
        self.invoker = None
        self.verbose = verbose

    def __trace(self, message):
        if self.verbose:
            print(message)

    def add_param(self, param_name, param_value):
        self.params[param_name] = param_value
        self.__trace("add param: name=%s, value=%s" % (param_name, param_value))

    def add_params(self, param_dict):
        for name, value in param_dict.items():
            self.add_param(name, value)

    def add_file(self, remote_file_name, local_file_name):
        with open(local_file_name, "rb") as f:
            self.files[remote_file_name] = StringIO(f.read().decode())
            self.__trace("add file: remote=%s, local=%s" % (remote_file_name, local_file_name))

    def add_files(self, file_dict):
        for remote, local in file_dict.items():
            self.add_file(remote, local)

    def init_job(self):
        if self.job is not None:
            return
        self.__trace("start init job ...")
        self.jenkins = Jenkins(self.url)
        self.job = self.jenkins[self.job_name]
        self.__trace("init job done")

    def last_build_number(self):
        if self.job is None:
            self.init_job()
        return self.job.get_last_good_buildnumber()

    def invoke(self, delay=1):
        if self.job is None:
            self.init_job()
        self.__trace("start invoke new build ...")
        self.invoker = self.job.invoke(block=True, build_params=self.params, files=self.files, delay=delay)
        self.__trace("new build was invoked")

    def wait_complete(self, timeout=60):
        if self.invoker is None:
            return
        if self.invoker.is_queued() or self.invoker.is_running():
            self.__trace("start wait build done ...")
            self.invoker.block_until_complete(delay=timeout)
            self.__trace("wait build done")

    def invoke_and_wait_complete(self, timeout=60):
        self.invoke()
        self.wait_complete(timeout=timeout)

    def download_artifacts(self, local_dir, force_download=True):
        if self.invoker is None:
            return

        artifacts = self.invoker.get_build().get_artifact_dict()

        for name, _ in artifacts.items():
            self.__trace("try to download remote file: %s" % name)

            local_file = os.path.sep.join([local_dir, os.path.basename(name)])

            if force_download and os.path.exists(local_file):
                os.remove(local_file)
                self.__trace("remove local file: %s" % local_file)
            try:
                artifacts[name].save_to_dir(local_dir)
            except ArtifactBroken:
                pass

            if os.path.exists(local_file):
                self.__trace("download local file success")
            else:
                self.__trace("download local file failed")


def jenkins_validate(clustername, web_type, localpath_to_artifact_dir, timeout='16', pull_method="LBMS", total_request="1000",
                     file_filter="", token="", jenkins_server = "http://10.148.183.183:8080/"):
    clustername_list = ["AMS", "DUS", "FRA", "LHR", "LAX", "SJC", "MDW", "DFW", "MIA", "EWR", "Wave2", "SIN", "HKG",
                        "SYD", "MEL", "LVSAZ01", "RNOAZ03", "SLCAZ01"]
    if clustername not in clustername_list:
        print("\033[1;35m%s is not a valid cluster name, please use one of them: %s!\033[0m" % (clustername, clustername_list))
        sys.exit("sorry, goodbye")

    jobname_list = [clustername, web_type, "L7PolicyValidator"]
    job_name = "-".join(jobname_list)

    validator = JenkinsApplication(jenkins_server, job_name)

    if web_type == "DWEB":
        validator.add_param("Timeout", timeout)
        validator.add_param("POP", clustername)
        validator.add_params({"Total_Requests": total_request, "L7_Rules_Pull_Method": pull_method})
        module_path = os.path.dirname(os.path.abspath(__file__))
        # default_filter_path = os.path.join(module_path, "filter_policies")
        # default_token_path = os.path.join(module_path, "kenstone_token")
        # if file_filter == "":
        #     file_filter = default_filter_path
        # if token == "":
        #     token = default_token_path

        #validator.add_file("EnvoyConfigGenerator/filter_policies.txt", file_filter)
        #validator.add_file("EnvoyConfigGenerator/keystone_token.txt", token)

    elif web_type == "MWEB":
        validator.add_params({"Total_Requests": total_request, "Timeout": timeout, "POP": clustername})
    else:
        print("\033[1;35m%s is invalid web type,please use DWEB or MWEB\033[0m!" % web_type)
        sys.exit("sorry, goodbye")

    validator.invoke_and_wait_complete(200)
    validator.download_artifacts(localpath_to_artifact_dir)


#jenkins_validate(clustername='AMS', web_type='scd', localpath_to_artifact_dir='/Users/xuenwang/validator_test/20201203')
if __name__ == '__main__':
    jenkins_validate(clustername='AMS', web_type='DWEB', localpath_to_artifact_dir='/Users/xuenwang/validator_test/20201203')
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--local_dir', type=str, default=".", help='local directory where to save downloaded files')
    # parser.add_argument('--POP_name', type=str, default="AMS", help="POP's name needs to be validated")
    # parser.add_argument('--web_type', type=str, default="DWEB", help="dweb or mweb")
    # parser.add_argument('--timeout', type=str, default="16", help="")
    # parser.add_argument('--total_request', type=str, default="0", help="")
    # parser.add_argument('--pull_method', type=str, default="STATIC", help="STATIC or LBMS")
    # parser.add_argument('--filter', type=str, default=" ", help="the local path of filter_policies.txt,such as /Users/dir/test")
    # parser.add_argument('--token', type=str, default=" ", help="the local path of keystone_token.txt,such as /Users/dir/test")
    #
    # args = parser.parse_args()
    # jobname_list = [args.POP_name, args.web_type, "L7PolicyValidator"]
    # job_name = "-".join(jobname_list)
    # print(job_name)
    #
    # validator = JenkinsApplication("http://10.148.183.183:8080/", job_name)
    # if args.web_type == "DWEB":
    #    validator.add_param("Timeout", args.timeout)
    #    validator.add_param("POP", args.POP_name)
    #
    #    validator.add_params({"Total_Requests": args.total_request, "L7_Rules_Pull_Method": args.pull_method})
    #
    #    validator.add_file("EnvoyConfigGenerator/filter_policies.txt", args.filter)
    #    validator.add_file("EnvoyConfigGenerator/keystone_token.txt", args.token)
    # elif args.web_type == "MWEB":
    #     validator.add_params({"Total_Requests": args.total_request, "Timeout": args.timeout, "POP": args.POP_name})
    #
    # validator.invoke_and_wait_complete(60)
    # validator.download_artifacts(args.local_dir)

