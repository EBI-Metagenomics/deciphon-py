struct dcp_output;
struct dcp_partition;
struct nmm_model;

struct dcp_output *dcp_output_create(char const *filepath, uint32_t nmodels);
int dcp_output_write(struct dcp_output *output, struct nmm_model const *model);
int dcp_output_destroy(struct dcp_output *output);
int dcp_output_close(struct dcp_output *output);

struct dcp_input *dcp_input_create(char const *filepath);
struct dcp_partition *dcp_input_create_partition(struct dcp_input const *input,
                                                 uint32_t partition,
                                                 uint32_t npartitions);
int dcp_input_destroy(struct dcp_input *input);

struct dcp_partition *dcp_partition_create(char const *filepath,
                                           uint64_t start_offset,
                                           uint32_t nmodels);
struct nmm_model const *dcp_partition_read(struct dcp_partition *part);
int dcp_partition_reset(struct dcp_partition *part);
bool dcp_partition_eof(struct dcp_partition const *part);
uint32_t dcp_partition_nmodels(struct dcp_partition const *part);
