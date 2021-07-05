/* DB */
struct dcp_db *dcp_db_openr(FILE *restrict fd);
struct dcp_db *dcp_db_openw(FILE *restrict fd, struct imm_abc const *abc);
int dcp_db_write(struct dcp_db *db, struct dcp_profile const *prof);
int dcp_db_close(struct dcp_db *db);
struct imm_abc const *dcp_db_abc(struct dcp_db const *db);
unsigned dcp_db_nprofiles(struct dcp_db const *db);
struct dcp_metadata dcp_db_metadata(struct dcp_db const *db, unsigned idx);
int dcp_db_read(struct dcp_db *db, struct dcp_profile *prof);
bool dcp_db_end(struct dcp_db const *db);

/* Metadata */
struct dcp_metadata
{
    char const *name;
    char const *acc;
};

static inline struct dcp_metadata dcp_metadata(char const *name,
                                               char const *acc);

/* Model */
enum dcp_model
{
    DCP_MODEL_ALT = 0,
    DCP_MODEL_NULL = 1
};
extern enum dcp_model const dcp_models[2];

/* Profile */
void dcp_profile_init(struct imm_abc const *abc, struct dcp_profile *prof);
void dcp_profile_deinit(struct dcp_profile *prof);

/* Server */
struct dcp_server *dcp_server_create(FILE *fd);
