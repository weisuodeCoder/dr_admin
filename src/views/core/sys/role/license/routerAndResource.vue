<template>
  <p style="font-size:12px;color:#f56c6c">
    <span>注:</span>
    &nbsp;&nbsp;默认颜色&nbsp;&nbsp;
    <span style="background-color:#000;">&nbsp;&nbsp;&nbsp;&nbsp;</span>
    &nbsp;&nbsp;为菜单项,颜色&nbsp;&nbsp;
    <span style="background-color:#358cd6;">&nbsp;&nbsp;&nbsp;&nbsp;</span>
    &nbsp;&nbsp;为页面资源！请选择页面资源，以免配置页面无法加载数据！
  </p>
  <el-divider />
  <!-- 提示内容！ -->
  <el-tree :data="routerList.val" ref="tree" :props="defaultProps" default-expand-all highlight-current show-checkbox node-key="id" :empty-text="isEmptyAll?'暂无数据':'无资源权限'">
    <template #default="{ node,data }">
      <el-row v-if="data.isButton">
        <el-col :span="23">
          <el-space :size="3">
            <el-text style="color:#358cd6;">{{node.label}}</el-text>
            <el-text>———</el-text>
            <el-text truncated size="small" style="color:#86c6fc;">{{data.description}}</el-text>
          </el-space>
        </el-col>
      </el-row>
      <el-row v-else>
        <el-col :span="23">
          <el-space :size="5">
            <el-text style="color: #000;">{{node.label}}</el-text>
            <el-text truncated size="small" style="color: #80858e;">——— {{data.description}}</el-text>
          </el-space>
        </el-col>
      </el-row>
    </template>
  </el-tree>
  <el-button type="warning" @click="getCheckedNodes">授权</el-button>
</template>
<script setup>
import router from '@/router';
import {
  ref,
  reactive,
  defineEmits,
  defineProps,
  watch,
  watchEffect,
} from 'vue';
import { ElMessage } from 'element-plus';
import { apiList, apiListAll, apiLicense } from '@/api/core/sys/license';

const props = defineProps(['pid']);
const tree = ref(null);
const routerList = reactive({ val: [] });

// tree显示数据
const defaultProps = {
  children: 'children',
  label: 'title',
  value: 'id',
  disabled: 'disabled',
  description: 'description',
};

// 请求数据
const onRefresh = () => {
  apiListAll().then((res) => {
    let routers = res.data.routers;
    let resources = res.data.resources;
    // 路由
    routerList.val = arr2tree(routers, 'id', 'pid', 'children');
    // 资源
    if (hasResource('/core/core/sys/license/list')) {
      traverseTree(routerList.val, resources, false); // 如果有权限，显示
    } else {
      traverseTree(routerList.val, resources, true); // 否则，禁用
      return ElMessage.error('权限不足！');
    }
    apiList({ id: props.pid }).then((res) => {
      let ids = [];
      res.data.ids.forEach((item) => {
        ids.push(item.id);
      });
      tree.value.setCheckedKeys(ids, false);
      console.log(routerList.val);
    });
  });
};

// 遍历树
function traverseTree(_tree, _arr, _disabled) {
  for (let i = 0; i < _tree.length; i++) {
    _tree[i].disabled = _disabled;
    if (_tree[i].isRouter == 1) {
      _tree[i].children.push(...addButton(_arr, _tree[i].id, _disabled));
    } else if (_tree[i].children.length > 0 && _tree[i].isButton == undefined) {
      traverseTree(_tree[i].children, _arr, _disabled);
    }
  }
}

// 添加按钮
function addButton(_arr, _pid, _disabled) {
  let newArr = [];
  for (let i = 0; i < _arr.length; i++) {
    if (_arr[i].pid == _pid) {
      let [temp] = _arr.splice(i, 1);
      temp.disabled = _disabled;
      temp.isButton = true;
      newArr.push(temp); // 删除_arr当中已匹配的内容
      i--; // 减去一个元素的同时应该同时减去索引
    }
  }
  return newArr;
}

// arr2tree算法(处理的数组: arr，主键: str，父id: str，children名字: str)
function arr2tree(_data, id, parentId, childName) {
  return _data.filter((father) => {
    let newArr = _data.filter((child) => {
      return father[id] === child[parentId];
    });
    father[childName] = newArr;
    return father[parentId] == 0;
  });
}

// 获取tree数据
const getCheckedNodes = () => {
  // getCheckedNodes(); true,true:返回子节点数组；false、true：返回父节点与子节点
  let all = tree.value.getCheckedNodes(false, true);
  let routers = [];
  let resources = [];
  for (let item of all) {
    if (item.isButton) {
      resources.push(item.id);
    } else {
      routers.push(item.id);
    }
  }
  let data = {
    id: props.pid,
    routers: routers,
    resources: resources,
  };
  apiLicense(data);
};

/**
 * @abstract: 页面资源
 */
const [isEmptyAll, isEmpty] = [ref(false), ref(false)];

watchEffect(() => {
  if (props.pid != 0 && props.pid != undefined) {
    if (hasResource('/core/core/sys/license/list-all')) {
      // 判断是否显示资源树
      onRefresh();
      isEmptyAll.value = true;
    }
  }
});
</script>
<style lang='scss' scoped>
.el-button {
  margin: 0;
}
.dr-dropdown-link {
  padding-left: 5px;
  padding-right: 5px;
  font-size: 22px;
  line-height: 7px;
  font-weight: bold;
  outline: 0;
  color: #ff9f1a;
}
.dr-dropdown-link:hover {
  outline: 0;
}
</style>