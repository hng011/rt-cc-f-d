install-hooks:
	@echo installing dev packages...
	@uv sync --group dev
	
	@echo installing pre-commit hook...
	@uv run pre-commit install
	
	@echo "--- ✅ Install complete! ---"
	@echo "--- IMPORTANT: Run 'ggshield auth login' manually if this is your first time. ---"


build-fraudapi-minikube:
	@export $$(grep -v '^#' ./fraudapi/.env | xargs) \
	&& eval $$(minikube docker-env) \
	&& echo building $$API_BASE_DIR:$${API_VERSION}-local ... \
	&& docker build -t $$API_BASE_DIR:$${API_VERSION}-local ./fraudapi/

build-dataflow-pipeline-minikube:
	@export $$(grep -v '^#' ./dataflow-pipeline/.env | xargs) \
	&& eval $$(minikube docker-env) \
	&& echo building $${SERVICE_NAME}:$${DFP_VERSION}-local ... \
	&& docker build -t $${SERVICE_NAME}:$${DFP_VERSION}-local ./dataflow-pipeline

build-fraudapi-gke:
	@export $$(grep -v '^#' ./fraudapi/.env | xargs) \
	&& echo building $$API_BASE_DIR:$${API_VERSION}-gke ... \
	&& docker build -t $$API_BASE_DIR:$${API_VERSION}-gke ./fraudapi/

update-fraudapi-image-tag:
	@export $$(grep -v '^#' ./fraudapi/.env | xargs) \
	&& echo creating new docker image tag: asia-southeast1-docker.pkg.dev/$$GOOGLE_PROJECT_ID/repo-hans/$$API_BASE_DIR:$${API_VERSION}-gke \
	&& docker tag $$API_BASE_DIR:$${API_VERSION}_local asia-southeast1-docker.pkg.dev/$$GOOGLE_PROJECT_ID/repo-hans/$$API_BASE_DIR:$${API_VERSION}-gke
	@docker images

push-latest-fraudapi-image-tag:
	@echo pushing to gcp artifact registery
	@export $$(grep -v '^#' ./fraudapi/.env | xargs) \
	&& echo latest image version: $$API_VERSION \
	&& docker push asia-southeast1-docker.pkg.dev/$$GOOGLE_PROJECT_ID/repo-hans/$$API_BASE_DIR:$${API_VERSION}-gke