def data():    
    return dict({
        "project": "Project",
        "file":"Project",
        "architecture": {
            "terraform": {
                "required_providers": {
                    "aws": {
                        "source": "hashicorp/aws"
                    }
                }
            },
            "provider": {
                "aws": {
                    "profile": "default",
                    "region": "us-east-1"
                }
            },
            "resource": {
                "aws_ecr_repository":{
                    "ecr_repository": {
                        "name" : "ecr-repository"
                    }
                },
                "aws_codebuild_project":{
                    "codebuild_project":{
                        "name": "test-project",
                        "description": "A project created by terraform",
                        "build_timeout": "10",
                        "service_role": "DatupCodeBuildRole",            
                        "artifacts": {
                            "type": "CODEPIPELINE"
                        },
                        "environment": {
                            "compute_type": "BUILD_GENERAL1_SMALL",
                            "image": "aws/codebuild/standard:2.0",
                            "type": "LINUX_CONTAINER",
                            "image_pull_credentials_type": "CODEBUILD",
                            "privileged_mode":True
                        },
                        "source": {
                            "type": "CODEPIPELINE",
                            "git_clone_depth": 0,
                            "insecure_ssl": False,
                            "report_build_status": False
                        }
                    }
                },
                "aws_s3_bucket":{
                    "project-datalake":{
                        "bucket":"project-datalake",
                        "acl":"private"
                    }
                },
                "aws_codecommit_repository":{
                    "project-repository":{
                        "repository_name":"project-repository",
                        "description":"This is a repository created by DatupieHW under Terraform",
                        "default_branch":"master"
                    }
                },
                "aws_s3_bucket_object":{
                    "dev_enviroment":{
                        "bucket":"project-datalake",
                        "key":"dev/",
                        "force_destroy":True
                    },
                    "dev_enviroment_clean":{
                        "bucket":"project-datalake",
                        "key":"dev/clean/",
                        "force_destroy":True
                    },
                    "dev_enviroment_prepare":{
                        "bucket":"project-datalake",
                        "key":"dev/prepare/",
                        "force_destroy":True
                    },
                    "dev_enviroment_transform":{
                        "bucket":"project-datalake",
                        "key":"dev/transform/",
                        "force_destroy":True
                    },
                    "dev_enviroment_inference":{
                        "bucket":"project-datalake",
                        "key":"dev/inference/",
                        "force_destroy":True
                    },
                    "dev_enviroment_data":{
                        "bucket":"project-datalake",
                        "key":"dev/data/",
                        "force_destroy":True
                    },
                    "prod_enviroment":{
                        "bucket":"project-datalake",
                        "key":"prod/",
                        "force_destroy":True
                    },
                    "prod_enviroment_inference":{
                        "bucket":"project-datalake",
                        "key":"prod/inference/",
                        "force_destroy":True
                    }
                }
            }
        }
    })