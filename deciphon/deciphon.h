/* Input */
struct dcp_input*         dcp_input_create(char const* filepath);
int                       dcp_input_destroy(struct dcp_input* input);
bool                      dcp_input_end(struct dcp_input const* input);
struct dcp_profile const* dcp_input_read(struct dcp_input* input);

/* Ouput */
int                dcp_output_close(struct dcp_output* output);
struct dcp_output* dcp_output_create(char const* filepath);
int                dcp_output_destroy(struct dcp_output* output);
int                dcp_output_write(struct dcp_output* output, struct nmm_profile const* prof);

/* Profile */
struct imm_abc const* dcp_profile_abc(struct dcp_profile const* prof);
void                  dcp_profile_destroy(struct dcp_profile const* prof, bool deep);
struct imm_model*     dcp_profile_get_model(struct dcp_profile const* prof, uint8_t i);
uint32_t              dcp_profile_id(struct dcp_profile const* prof);
uint8_t               dcp_profile_nmodels(struct dcp_profile const* prof);

/* Result */
imm_float                dcp_result_alt_loglik(struct dcp_result const* result);
struct imm_result const* dcp_result_alt_result(struct dcp_result const* result);
char const*              dcp_result_alt_stream(struct dcp_result const* result);
void                     dcp_result_destroy(struct dcp_result const* result);
imm_float                dcp_result_null_loglik(struct dcp_result const* result);
struct imm_result const* dcp_result_null_result(struct dcp_result const* result);
uint32_t                 dcp_result_profid(struct dcp_result const* result);
