struct dcp_output;

struct dcp_output *dcp_output_create(char const *filepath, uint32_t nmodels);
int dcp_output_write(struct dcp_output *output, struct nmm_model const *model);
int dcp_output_destroy(struct dcp_output *output);
int dcp_output_close(struct dcp_output *output);
