<template>
  <Dialog :title="title" ref="show" width="500" :info="info">
    <template #body>
      <el-form :model="info.val" label-width="80" label-position="left" :rules="rules" ref="from">
        <el-row :gutter="30">
          <el-col :span="23">
            <el-form-item label="职位名称" prop="name">
              <el-input clearable :disabled="disabled" v-model="info.val.name" placeholder="请输入职位名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="30">
          <el-col>
            <el-form-item label="组织" prop="orgId">
              <el-tree-select filterable :disabled="disabled||type=='update'" v-model="info.val.orgId" :props="defaultProps" :data="list.val" check-strictly @node-click="onRoleNodeClick" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="30">
          <el-col>
            <el-form-item label="排序" prop="sort">
              <el-input-number v-model="info.val.sort" :min="1" controls-position="right" />
            </el-form-item>
          </el-col>
        </el-row>
        <!-- <el-row :gutter="30">
          <el-col>
            <el-form-item label="标识" prop="tag">
              <el-select @change="onSelectChange" v-model="info.val.level" placeholder="请选择等级" :disabled="disabled">
                <el-option label="管理员" :value="2" />
                <el-option label="普通用户" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row> -->
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
import { apiList as orgApiList } from '@/api/core/sys/org';
import {
  ref,
  reactive,
  inject,
  watch,
  defineEmits,
  defineExpose,
  computed,
} from 'vue';
import Dialog from '@/components/tools/dialog.vue';
import { apiCreate, apiUpdate, apiShow } from '@/api/core/sys/role';
import { ElMessage } from 'element-plus';
import { matchingFalse } from '@/tools/rules';

const emits = defineEmits(['onChange']);
const data = inject('_data');

const list = reactive({ val: [] }); // 机构
const info = reactive({ val: {} });
const show = ref(null);
const from = ref(null);
const title = ref('');
let type = 'show';
let disabled = false;
let id = 0;

// 验证规则
const rules = reactive({
  name: [
    { required: true, message: '内容不能为空', trigger: 'blur' },
    { validator: matchingFalse.notEmpty, trigger: 'blur' },
  ],
  orgId: [{ required: true, message: '内容不能为空', trigger: 'change' }],
});

// tree默认显示数据
const defaultProps = {
  children: 'children',
  label: 'name',
  value: 'id',
};

// 显示
const onShow = (_id, _type) => {
  id = _id;
  type = _type;
  let join = '';
  if (_type == 'create') {
    // info.val.level = 3;
    disabled = false;
    join = '创建';
  } else if (_type == 'show') {
    disabled = true;
    join = '查看';
  } else if (_type == 'update') {
    disabled = false;
    join = '更新';
  }
  title.value = '职位__' + join;
  onRefresh();
  show.value.onShow();
};

// 获取初始化数据
const onRefresh = () => {
  if (id != 0) {
    apiShow(id).then((res) => {
      info.val = res.data;
    });
  }
  let data = {
    pageSize: 10000,
  };
  orgApiList(data).then((res) => {
    list.val = arr2tree(res.data.list, 'id', 'pid', 'children');
  });
};

// 当选中上级机构时
const onRoleNodeClick = (_data, node) => {
  info.val.orgName = _data.name;
};

// arr2tree算法
function arr2tree(_data, _id, _parentId, _childName) {
  return _data.filter((father) => {
    let newArr = _data.filter((child) => {
      return father[_id] === child[_parentId];
    });
    father[_childName] = newArr;
    return father[_parentId] == 0;
  });
}

// 提交按钮逻辑
const doSubmit = (rule) => {
  if (type == 'show') {
    show.value.onClose();
  }
  if (!rule) return;
  rule.validate((valid) => {
    if (valid) {
      if (type == 'create') {
        // create
        apiCreate(info.val).then((res) => {
          show.value.onClose();
          emits('onChange');
        });
      } else if (type == 'update') {
        // update
        apiUpdate(info.val).then((res) => {
          show.value.onClose();
          emits('onChange');
        });
      }
    } else {
      return false;
    }
  });
};

// 获取按钮名称
const getName = computed(() => {
  return () => {
    let name = '';
    if (type == 'create') {
      name = '创建';
    } else if (type == 'show') {
      name = '确定';
    } else if (type == 'update') {
      name = '更新';
    }
    return name;
  };
});

defineExpose({ onShow });
</script>
<style lang='scss' scoped>
</style>