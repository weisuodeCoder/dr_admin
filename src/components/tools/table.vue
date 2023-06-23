<template>
  <el-table :row-key="rowKey" border stripe :data="list.val" style="width: 100%" @selection-change="selectionChangeHandle" :default-expand-all="open=='true'" :empty-text="emptyText">
    <template v-for="(item, i) in columns" :key="i">
      <el-table-column v-if="item.type != undefined" :width="item.width" :prop="item.prop" :type="item.type">
        <template v-if="item.slot!=undefined" #default="scope">
          <slot :name="item.slot" :row="scope.row"></slot>
        </template>
      </el-table-column>
      <el-table-column show-overflow-tooltip v-else :sortable="item.sortable" :prop="item.prop" :width="item.width" :label="item.label" :fixed="item.fixed">
        <template #default="scope">
          <slot v-if="item.slot!=undefined" :name="item.slot" :row="scope.row"></slot>
        </template>
      </el-table-column>
    </template>
  </el-table>
  <!-- 列表底部 -->
  <div class="dr-clearfix dr-footer">
    <!-- 列表批量操作 -->
    <div class="dr-all">
      <slot name="all"></slot>
    </div>
    <!-- 分页 -->
    <template v-if="tree==undefined">
      <el-pagination v-if="pageType=='small'" class="dr-pager" v-model:current-page="params.pager.pageNum" v-model:page-size="params.pager.pageSize" :page-sizes="[10, 20, 30, 50]" background layout=" total,prev, pager, next,jumper" :total="total" :pager-count="5" small @size-change="pageSizeChange" @current-change="pageCurrentChange" />
      <el-pagination v-else class="dr-pager" v-model:current-page="params.pager.pageNum" v-model:page-size="params.pager.pageSize" :page-sizes="[10, 20, 30, 50]" background layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="pageSizeChange" @current-change="pageCurrentChange" />
    </template>
  </div>
</template>
<script setup>
import { ref, reactive, defineEmits, toRefs, watch, onMounted } from 'vue';
import $api from '../../api/api';

// 下一步动作，操作以及批量操作功能实现
const props = defineProps([
  'columns', // 列表项
  'params', // 请求参数
  'lasy', // 延迟请求
  'tree', // 是否为树？是的话不显示pager
  'rowKey', // 默认为id可修改
  'open', // 是否展开行
  'emptyText', // 内容为空时显示的文字
  'pageType', // 设置分页器的大小
]);
const list = reactive({ val: [] });

let rowKey = 'id';
let total = 0;
let columns = props.columns;

// 获取列表数据
const onRefresh = () => {
  let params = props.params;
  if (params.url == undefined || params.url == '') return;
  let config = {};
  for (let key in params) {
    if (key != 'url') {
      if (key == 'pager') {
        config['pageSize'] =
          params[key].pageSize == undefined ? 10 : params[key].pageSize;
        config['pageNum'] =
          params[key].pageNum == undefined ? 1 : params[key].pageNum;
      } else {
        config[key] = params[key];
      }
    }
  }
  $api.post(params.url, config).then((res) => {
    if (res.success) {
      if (props.tree == undefined || props.tree.id == undefined) {
        list.val = res.data.list;
        total = res.data.total;
      } else {
        list.val = arr2tree(
          res.data.list,
          'id',
          props.tree.name,
          'children',
          props.tree.id
        );
        total = res.data.total;
      }
    }
  });
};

// arr2tree算法(处理的数组: arr，主键: str，父id: str，children名字: str，筛选条件：str)
function arr2tree(_datas, _id, _parentId, _childName, _condition) {
  return _datas.filter((father) => {
    let newArr = _datas.filter((child) => {
      return father[_id] === child[_parentId];
    });
    father[_childName] = newArr;
    return father[_id] == _condition; // 返回条件，根目录id与请求id相同
  });
}

// table多选动作
let ids = [];
const selectionChangeHandle = (rows) => {
  ids = [];
  for (let row of rows) {
    ids.push(row.id);
  }
};

const getIds = () => {
  return ids;
};

// 分页器动作
const pageSizeChange = (val) => {
  props.params.pager.pageSize = val;
  onRefresh();
};
const pageCurrentChange = (val) => {
  props.params.pager.pageNum = val;
  onRefresh();
};

onMounted(() => {
  if (props.lasy == undefined) {
    onRefresh();
  }
  if (props.rowKey != undefined) {
    rowKey = props.rowKey;
  }
});

defineExpose({ getIds, onRefresh });
</script>
<style lang="scss" scoped>
.dr-button {
  float: left;
}
.dr-footer {
  margin-top: 20px;
}
.dr-pager {
  float: right;
}
.dr-all {
  float: left;
  display: flex;
  flex-direction: row;
  justify-content: start;
}
</style>