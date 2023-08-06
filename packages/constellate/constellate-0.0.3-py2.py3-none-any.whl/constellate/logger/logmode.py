from enum import IntFlag


class LogMode(IntFlag):
    # Environment
    ENV_PRODUCTION = 1
    ENV_STAGING = 2
    ENV_LOCAL = 4
    # Interactive
    INTERACTIVE_YES = 8
    INTERACTIVE_NO = 16
    # Level of details
    DETAIL_NORMAL = 32
    DETAIL_TRACE = 64
    # Server+Client or Standalone Logger
    OPERATE_STANDALONE = 128
    OPERATE_SERVER = 256
    OPERATE_CLIENT = 512
