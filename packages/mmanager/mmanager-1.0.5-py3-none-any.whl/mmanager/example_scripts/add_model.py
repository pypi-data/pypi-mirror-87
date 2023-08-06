from mmanager.mmanager import Model

secret_key = "Secret-Key"

url = 'http://app.modelmanager.ai'
path =  'api_assets'
#for data
data = {
    "project": "Project_id",
    "transformerType": "logistic",
    "target_column": "id",
    "note": "api script Model",
    "model_area": "api script Model",
    "model_dependencies": "api script Model",
    "model_usage": "api script Model",
    "model_adjustment": "api script Model",
    "model_developer": "api script Model",
    "model_approver": "api script Model",
    "model_maintenance": "api script Model",
    "documentation_code": "api script Model",
    "implementation_plateform": "api script Model",
    "training_dataset": "%s/model_assets/train.csv" % path,
    "pred_dataset": "%s/model_assets/submissionsample.csv" % path,
    "actual_dataset": "%s/model_assets/truth.csv" % path,
    "test_dataset": "%s/model_assets/test.csv" % path,
    "model_image_path":"%s/model_assets/model_image.jpg" % path,
    "model_summary_path":"%s/model_assets/summary.json." % path,
    "model_file_path": "%s/model_assets/model_file_path.json" % path,
    "scoring_file_path":"", #Not Required
    "production":"", #Not Required
    "current_date":"", #Not Required
}

try:
    Model(secret_key, url).post_model(data)
except Exception as e:
    print(str(e))

        