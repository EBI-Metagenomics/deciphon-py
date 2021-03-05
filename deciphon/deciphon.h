/* Input */
int                       dcp_input_close(struct dcp_input* input);
struct dcp_input*         dcp_input_create(char const* filepath);
int                       dcp_input_destroy(struct dcp_input* input);
bool                      dcp_input_end(struct dcp_input const* input);
struct dcp_profile const* dcp_input_read(struct dcp_input* input);

/* Ouput */
int                dcp_output_close(struct dcp_output* output);
struct dcp_output* dcp_output_create(char const* filepath);
int                dcp_output_destroy(struct dcp_output* output);
int                dcp_output_write(struct dcp_output* output, struct dcp_profile const* prof);

/* Profile */
struct imm_abc const*     dcp_profile_abc(struct dcp_profile const* prof);
void                      dcp_profile_append_model(struct dcp_profile* prof, struct imm_model* model);
struct dcp_profile*       dcp_profile_create(struct imm_abc const* abc);
void                      dcp_profile_destroy(struct dcp_profile const* prof, bool deep);
void                      dcp_profile_free(struct dcp_profile const* prof);
struct imm_model*         dcp_profile_get_model(struct dcp_profile const* prof, uint8_t i);
uint32_t                  dcp_profile_id(struct dcp_profile const* prof);
struct nmm_profile const* dcp_profile_nmm_profile(struct dcp_profile const* prof);
uint8_t                   dcp_profile_nmodels(struct dcp_profile const* prof);

void dcp_profile_setup(struct imm_hmm* hmm, struct imm_dp* dp, bool multiple_hits, uint32_t target_length,
                       bool hmmer3_compat);

/* Result */
imm_float                dcp_result_alt_loglik(struct dcp_result const* result);
struct imm_result const* dcp_result_alt_result(struct dcp_result const* result);
char const*              dcp_result_alt_stream(struct dcp_result const* result);
void                     dcp_result_destroy(struct dcp_result const* result);
imm_float                dcp_result_null_loglik(struct dcp_result const* result);
struct imm_result const* dcp_result_null_result(struct dcp_result const* result);
uint32_t                 dcp_result_profid(struct dcp_result const* result);
