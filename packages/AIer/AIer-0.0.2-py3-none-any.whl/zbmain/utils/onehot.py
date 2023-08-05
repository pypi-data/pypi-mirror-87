from numpy import argmax


class OneHot(object):
    '''
    onehot生成器
    编码：call() || encode()
    解码：decode()
    '''

    def __init__(self):
        # 总类别特征列表
        self.__class_lst = []
        # 编码映射表
        self.__char_to_num = []
        # 源码映射表
        self.__num_to_char = []
        # onehot编码列表
        self.__onehot_encoded = []

    def __call__(self, sourceList:list, classList:list=None):
        '''
        列表 转 onehot编码
        :param sourceList: 源列表
        :param classList: 源列表总特征表。缺省：None（则等于源列表）
        :return:onehot编码列表
        '''
        return self.encode(sourceList, classList)

    def encode(self, sourceList:list, classList:list=None):
        '''
        列表 转 onehot编码（与call方法等价）
        :param sourceList: 源列表
        :param classList: 源列表总特征表。缺省：None（None则为源列表）
        :return:onehot编码列表
        '''
        self.__class_lst = classList or sourceList #没有指定总类型表,则当前列表为总类型
        self.__char_to_num = dict((c, n) for n, c in enumerate(self.__class_lst))
        self.__num_to_char = dict((n, c) for n, c in enumerate(self.__class_lst))
        integer_encoded = [self.__char_to_num[char] for char in sourceList]
        # onehot编码数组
        self.__onehot_encoded = []
        for value in integer_encoded:
            letter = [0 for _ in range(len(self.__class_lst))]
            letter[value] = 1
            self.__onehot_encoded.append(letter)
        return self.__onehot_encoded

    def decode(self, onehotNode:list):
        '''
        onehot编码元素 转 源列表元素
        :param onehotNode: onehot编码返回的元素
        :return:源列表元素
        :example: decode([1,0,0])
        '''
        return self.__num_to_char[argmax(onehotNode)]

    def getNodeOneHot(self, char:str):
        '''
        源列表元素 获取 onehot编码元素
        :param char: 编码源元素
        :return: 该元素的onehot编码
        '''
        return self.__onehot_encoded[self.__char_to_num[char]]

    @property
    def onehotCode(self):
        '''获取onehot码'''
        return self.__onehot_encoded


if __name__ == "__main__":
    onehot = OneHot()
    source = ['a', 'b', 'c', 'd']
    onehot_list = onehot(source)
    print(onehot_list)
    print(onehot.getNodeOneHot(source[1]))
    print(onehot.decode(onehot_list[1]))
