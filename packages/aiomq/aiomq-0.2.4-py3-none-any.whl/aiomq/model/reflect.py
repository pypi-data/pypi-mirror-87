"""
反射数据类源-规则
最晚3秒检测一次

"""
from datetime import datetime


class ReflectSource(object):
    def __init__(self, parent, listen_keys, reflect):
        self.parent = parent
        self.reflect = reflect or {}
        self.listen_keys = listen_keys or []
        self.listen_callback_dict = {}
        for field in self.listen_keys:
            setattr(self, field, None)

    def listen(self, key, callback):
        if key in self.listen_keys:
            self.listen_callback_dict[key] = callback

    def __setattr__(self, key, value):
        super(ReflectSource, self).__setattr__(key, value)
        if hasattr(self, 'listen_keys'):
            if key in self.reflect:
                key = self.reflect[key]
                value = getattr(self, key)
            if key in self.listen_keys:
                print('这里发出事件')
                if key in self.listen_callback_dict:
                    self.listen_callback_dict[key](value)

    def __str__(self):
        return f"<Data {self.parent.__name__} {' '.join([f'{key}={getattr(self, key)}' for key in self.listen_keys])}>"


class Field(object):
    ttype = None

    def __init__(self, label='', default=None):
        # self.name = name
        self.label = label
        self.default = default


class StringField(Field):
    ttype = str


class IntegerField(Field):
    ttype = int


class FloatField(Field):
    ttype = float


class BooleanField(Field):
    ttype = bool


class DateTimeField(Field):
    ttype = datetime


class ReflectModel(object):
    class Meta:
        verbose_name_plural = verbose_name = __name__

    @classmethod
    def Singleton(cls):
        def initialization():
            listen_keys = []
            reflect = {}
            for key in dir(cls):
                value = getattr(cls, key)
                if isinstance(value, Field):
                    listen_keys.append(key)
                    if hasattr(value, 'reflect'):
                        reflect[key] = getattr(value, 'reflect')
            return ReflectSource(cls, listen_keys, reflect)

        if not hasattr(cls, 'singleton'):
            cls.singleton = initialization()
        return cls.singleton


if __name__ == '__main__':
    class TaskData(ReflectModel):
        name = StringField('名字', default='孙')
        age = IntegerField('年龄')


    task_data = TaskData.Singleton()
    task_data.name = '孙乾翔'
    task_data.age = 21
    print(TaskData.Singleton())
