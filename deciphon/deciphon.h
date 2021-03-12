/* Input */
int                        dcp_input_close(struct dcp_input* input);
struct dcp_input*          dcp_input_create(char const* filepath);
int                        dcp_input_destroy(struct dcp_input* input);
bool                       dcp_input_end(struct dcp_input const* input);
struct dcp_metadata const* dcp_input_metadata(struct dcp_input const* input, uint32_t profid);
uint32_t                   dcp_input_nprofiles(struct dcp_input const* input);
struct dcp_profile const*  dcp_input_read(struct dcp_input* input);
int                        dcp_input_reset(struct dcp_input* input);

/* Metadata */
char const*          dcp_metadata_acc(struct dcp_metadata const* mt);
struct dcp_metadata* dcp_metadata_create(char const* name, char const* acc);
void                 dcp_metadata_destroy(struct dcp_metadata const* mt);
char const*          dcp_metadata_name(struct dcp_metadata const* mt);

/* Ouput */
int                dcp_output_close(struct dcp_output* output);
struct dcp_output* dcp_output_create(char const* filepath);
int                dcp_output_destroy(struct dcp_output* output);
int                dcp_output_write(struct dcp_output* output, struct dcp_profile const* prof);

/* Profile */
struct imm_abc const*      dcp_profile_abc(struct dcp_profile const* prof);
void                       dcp_profile_append_model(struct dcp_profile* prof, struct imm_model* model);
struct dcp_profile*        dcp_profile_create(struct imm_abc const* abc, struct dcp_metadata const* mt);
void                       dcp_profile_destroy(struct dcp_profile const* prof, bool deep);
void                       dcp_profile_free(struct dcp_profile const* prof);
uint32_t                   dcp_profile_id(struct dcp_profile const* prof);
struct dcp_metadata const* dcp_profile_metadata(struct dcp_profile const* prof);
struct imm_model*          dcp_profile_model(struct dcp_profile const* prof, uint8_t i);
struct nmm_profile const*  dcp_profile_nmm_profile(struct dcp_profile const* prof);
uint8_t                    dcp_profile_nmodels(struct dcp_profile const* prof);

/* Result */
imm_float                dcp_result_alt_loglik(struct dcp_result const* result);
struct imm_result const* dcp_result_alt_result(struct dcp_result const* result);
char const*              dcp_result_alt_stream(struct dcp_result const* result);
char const*              dcp_result_alt_codon_stream(struct dcp_result const* result);
void                     dcp_result_destroy(struct dcp_result const* result);
imm_float                dcp_result_null_loglik(struct dcp_result const* result);
struct imm_result const* dcp_result_null_result(struct dcp_result const* result);
char const*              dcp_result_null_stream(struct dcp_result const* result);
char const*              dcp_result_null_codon_stream(struct dcp_result const* result);
uint32_t                 dcp_result_profid(struct dcp_result const* result);
uint32_t                 dcp_result_seqid(struct dcp_result const* result);

/* Results */
void                     dcp_results_destroy(struct dcp_results const* results);
struct dcp_result const* dcp_results_first(struct dcp_results const* results);
struct dcp_result const* dcp_results_next(struct dcp_results const* results, struct dcp_result const* result);

/* Server */
struct dcp_server*         dcp_server_create(char const* filepath);
void                       dcp_server_destroy(struct dcp_server const* server);
struct dcp_metadata const* dcp_server_metadata(struct dcp_server const* server, uint32_t profid);
uint32_t                   dcp_server_nprofiles(struct dcp_server const* server);
void                       dcp_server_scan(struct dcp_server* server, struct dcp_task* task);

/* Task */
struct dcp_task_cfg
{
    bool loglik;
    bool null;
    bool multiple_hits;
    bool hmmer3_compat;
};

void                      dcp_task_add(struct dcp_task* task, char const* sequence);
struct dcp_task*          dcp_task_create(struct dcp_task_cfg cfg);
void                      dcp_task_destroy(struct dcp_task const* task);
void                      dcp_task_reset(struct dcp_task* task);
struct dcp_results const* dcp_task_results(struct dcp_task const* task);
