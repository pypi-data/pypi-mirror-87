# ufes-tess-validator
The repository for performing automatic validation for tess upgrades of UFES clusters
 
## jenkins_validate 
The package is used to trigger a validator job in jenkins(http://10.148.183.183:8080/  may be other server IP), after building finished,it can also download artifacts.

## how to use it
### install packages
```pip install jenkinsapi
   pip install jenkins-validate==0.0.1
```
### put the follow commands into a python script:
```import jenkins_validate
   from jenkins_validate import auto_validator
   auto_validator.jenkins_validate()   
   #input the parameters,"clustername","web_type"and "localpath_to_artifact_dir" are the Required parameters 
```
### then run the python script.

