<template>
  <Dialog :title="title" ref="show" width="600" :info="info">
    <template #body>
      <el-form :model="info.val" label-width="80" label-position="left" :rules="rules" ref="from">
        <el-row :gutter="20">
          <el-col>
            <el-form-item label="组织名称" prop="name">
              <el-input clearable :disabled="disabled" v-model="info.val.name" placeholder="请输入组织名称" />
            </el-form-item>
          </el-col>

        </el-row>
        <el-row :gutter="20">
          <el-col>
            <el-form-item label="上级组织" prop="pid">
              <el-tree-select filterable :disabled="disabled" v-model="info.val.pid" :props="defaultProps" :data="list.val" check-strictly @node-click="onNodeClick" />
              <el-tooltip class="box-item" effect="dark" content="跟组织" placement="right">
                <el-button style="margin-left: 10px" size="small" type="danger" :icon="Delete" circle @click="onClear" />
              </el-tooltip>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col>
            <el-form-item label="排序" prop="sort">
              <el-input-number :disabled="disabled" v-model="info.val.sort" :min="1" controls-position="right" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </template>
    <template #button>
      <el-button size="small" type="success" @click="doSubmit(from)">
        {{ getName() }}
      </el-button>
    </template>
  </Dialog>
</template>
<script setup>
import { Delete } from '@element-plus/icons-vue';
import {
  ref,
  reactive,
  defineProps,
  defineEmits,
  defineExpose,
  toRefs,
  computed,
  watchEffect,
} from 'vue';
import Dialog from '@/components/tools/dialog.vue';
import { apiCreate, apiUpdate, apiShow, apiList } from '@/api/core/sys/org';
import { ElMessage } from 'element-plus';

const props = defineProps(['data']);
const emits = defineEmits(['onChange']);
const show = ref(null);
const from = ref(null);
const info = reactive({ val: {} });
const title = ref('');
const list = reactive({ val: [] });
let id = 0;
let type = 'show';
let state = false;
let disabled = false;

// tree组件默认显示数据
const defaultProps = {
  children: 'children',
  label: 'name',
  value: 'id',
};

// 验证规则
const rules = reactive({
  name: [{ required: true, message: '内容不能为空', trigger: 'blur' }],
});

// 显示
const onShow = (_id, _type) => {
  id = _id;
  type = _type;
  let join = '';
  if (_type == 'create') {
    disabled = false;
    join = '创建';
  } else if (_type == 'show') {
    disabled = true;
    join = '查看';
  } else if (_type == 'update') {
    disabled = false;
    join = '更新';
  }
  title.value = '组织层级__' + join;
  onRefresh();
  show.value.onShow();
};

// 清空tree选择框
const onClear = () => {
  info.val.router = 'root';
  info.val.pid = 0;
  state = true;
};

// 获取数据
const onRefresh = () => {
  // 获取列表数据
  apiList({ pageSize: 10000 }).then((res) => {
    // res.data.list.forEach((item,x)=> {
    //   if(item.id == id) {
    //     res.data.list.splice(x,1);
    //   }
    // });
    let lis = arr2tree(res.data.list, 'id', 'pid', 'children');
    list.val = lis;
  });
  // 获取当前项数据
  if (id != 0 && id != undefined) {
    apiShow(id).then((res) => {
      info.val = res.data;
    });
  }
};

// 提交按钮逻辑
const doSubmit = (rule) => {
  if (!rule) return;
  if (type == 'show') {
    show.value.onClose();
  }
  rule.validate((valid) => {
    if (valid) {
      if (type == 'create') {
        // create
        console.log(info.val.rows);
        delete info.val.rows;
        apiCreate(info.val).then((res) => {
          info.val = {};
          show.value.onClose();
          emits('onChange');
        });
      } else if (type == 'update') {
        // update
        // 如果点击tree组件并且rows不为空时
        if (state && info.val.rows != undefined) {
          info.val.rows.forEach((item, x) => {
            if (info.val.id == item.id) {
              // 删除本身
              info.val.rows.splice(x, 1);
            }
          });
          info.val.rows.forEach((item, x) => {
            // 修改rows路由
            let index = item.router.indexOf(info.val.id);
            if (index != -1) {
              let path =
                info.val.router +
                '/' +
                item.router.slice(index, item.router.length);
              info.val.rows[x].router = path;
            } else {
              console.log(item.id, '----', index);
            }
          });
        } else {
          // 若未点击或者rows为空时删除rows
          delete info.val.rows;
        }
        if (info.val.pid == info.val.id) {
          // 禁止选择本身，并且修改路由
          state = false;
          info.val.rows.forEach((item, x) => {
            let str = item.router.replace('/' + info.val.id, '');
            info.val.rows[x].router = str;
          });
          return ElMessage.error({ message: '不能选择自身' });
        }
        apiUpdate(info.val).then((res) => {
          state = false;
          info.val = {};
          show.value.onClose();
          emits('onChange');
        });
      }
    } else {
      return false;
    }
  });
};

// 获取父id
const getParent = (node) => {
  let pids = [];
  if (node.parent && node.parent.data.id) {
    pids.push(node.parent.data.id);
    pids.push(...getParent(node.parent));
  }
  return pids;
};

// 当点击tree-select时
const onNodeClick = (_data, node) => {
  state = true;
  // 生成路径：router
  let pids = getParent(node).reverse();
  pids = pids.join('/');
  pids = !pids
    ? 'root' + pids + '/' + _data.id
    : 'root/' + pids + '/' + _data.id;
  info.val.router = pids;
};

// arr2tree算法
function arr2tree(_data, _id, _parentId, _childName) {
  return _data.filter((father) => {
    if (id != 0) {
      if (father.id == id || father.router.indexOf(id) != -1) {
        father.disabled = true;
      }
    }
    let newArr = _data.filter((child) => {
      return father[_id] === child[_parentId];
    });
    father[_childName] = newArr;
    return father[_parentId] == 0;
  });
}

// 获取按钮名称
const getName = computed(() => {
  return () => {
    let name = '';
    if (type == 'create') {
      name = '创建';
    } else if (type == 'show') {
      name = '查看';
    } else if (type == 'update') {
      name = '更新';
    }
    return name;
  };
});

// 获取子路由
const getChildRouter = (_data) => {
  let arr = [];
  arr.push({ id: _data.id, router: _data.router });
  _data.children.forEach((item, x) => {
    if (item.children.length > 0) {
      arr.push(...getChildRouter(item));
    } else {
      arr.push({ id: item.id, router: item.router });
    }
  });
  return arr;
};

defineExpose({ onShow });

watchEffect(() => {
  if (JSON.stringify(props.data) != '{}' && props.data.children.length > 0) {
    info.val.rows = getChildRouter(props.data);
  }
});
// // 获取子id
// const getIds = (_data, level) => {
//   let ids = [];
//   ids.push({ id: _data.id, level: level });
//   level++;
//   if (_data.children.length > 0) {
//     _data.children.forEach((el) => {
//       ids.push(getIds(el, level));
//     });
//   }
//   return ids;
// };

// // 获取子路由
// let childPath = []; // 子路由路径
// let levelPath = [];
// const getChildRouter = (arr) => {
//   arr.forEach((item, x) => {
//     if (item instanceof Array) {
//       getChildRouter(item, childPath[item.level]);
//     } else {
//       levelPath[item.level] = item.id;
//       let parentPath = "";
//       for (let i = 1; i < item.level + 1; i++) {
//         parentPath += "/" + levelPath[i];
//       }
//       childPath.push({ router: info.val.router + parentPath, id: item.id });
//     }
//   });
// };
</script>
<style lang="scss" scoped>
</style>