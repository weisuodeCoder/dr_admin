import { ElPopperArrow } from "element-plus";

/**
 * 字符串验证规则
 */
export const matchingFalse = {
    // 不匹配中文
    notChince: (_rule, _val, _callBack) => {
        console.log(_rule);
        let reg = /[\u4e00-\u9fa5]/;
        if (reg.test(_val)) {
            return new Error('不能含有汉字');
        }
        _callBack();
    },
    // 不匹配空
    notEmpty: (_rule, _val, _callBack) => {
        let reg = /[\/\s|\/\n]/;
        if (reg.test(_val)) {
            return new Error('不能含有空格和换行符')
        } else {
            _callBack();
        }
    }
}

export const matchingSome = {
    // 匹配账号
    isAccount: (_rule, _val, _callBack) => {
        let reg = /^[a-zA-Z][a-zA-Z0-9_]*$/;
        if (reg.test(_val)) {
            _callBack();
        } else {
            return new Error('字母开头,由字母数字下划线组成')
        }
    },
}