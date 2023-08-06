# 本配置文件的异常基类
class ConfigError(Exception):
    pass


class BackGround_Error(ConfigError):
    def __init__(self, info=''):
        self.info = info

    def __str__(self):
        return "背景实现错误！{}".format(self.info)


class Action_Error(ConfigError):
    def __init__(self, info=''):
        self.info = info

    def __str__(self):
        return "动作类发生错误！{}".format(self.info)


class Role_Error(ConfigError):
    def __init__(self, info=''):
        self.info = info

    def __str__(self):
        return "角色类发生错误！{}".format(self.info)

class Fall_Error(ConfigError):
    def __init__(self, info=''):
        self.info = info

    def __str__(self):
        return "下落物体类发生错误！{}".format(self.info)