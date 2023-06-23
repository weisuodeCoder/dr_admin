<template>
  <el-dialog fullscreen :destroy-on-close="true" v-model="isShow" @close="closeDialog" :append-to-body="true" class="dr-global-dialog-padding10">
    <!-- 头部功能区 -->
    <template #header>
      <el-text class="dr-label" style="margin-left:10px;">截图框宽度比</el-text>
      <el-input-number :disabled="props.options.disabled" v-model="options.fixedNumber[0]" @change="onChange(0)" :min="1" controls-position="right" />
      <el-text class="dr-label">截图框高度比</el-text>
      <el-input-number :disabled="props.options.disabled" v-model="options.fixedNumber[1]" @change="onChange(1)" :min="1" controls-position="right" />
      <el-text class="dr-label">固定比例</el-text>
      <el-switch :disabled="props.options.disabled" v-model="options.fixed" inline-prompt active-text="是" inactive-text="否" />
      <el-text class="dr-label">允许滚轮缩放</el-text>
      <el-switch v-model="options.canScale" inline-prompt active-text="是" inactive-text="否" />
      <el-text class="dr-label" style="">是否允许拖动</el-text>
      <el-switch v-model="options.canMove" inline-prompt active-text="是" inactive-text="否" />
      <el-text class="dr-label" type="warning" style="margin-left:60px;">
        ⚠ 按Esc、点击右上角关闭按钮或取消均可退出裁剪模式。
      </el-text>
    </template>
    <!-- 裁剪视图区 -->
    <div class="avatar-crop" ref="cropBox">
      <vueCropper class="crop-box" ref="cropper" :img="options.img" :autoCrop="options.autoCrop" :fixedBox="options.fixedBox" :canMoveBox="options.canMoveBox" :autoCropWidth="options.autoCropWidth" :autoCropHeight="options.autoCropHeight" :centerBox="options.centerBox" :fixed="options.fixed" :fixedNumber="options.fixedNumber" :canMove="options.canMove" :canScale="options.canScale"></vueCropper>
    </div>
    <!-- 底部操作区 -->
    <template #footer>
      <div style="text-align:center;">
        <el-button color="#d9d9d9" size="large" @click="isShow=false" :icon="Close" style="font-size: 18px;margin-right:40px;">取 消</el-button>
        <el-button color="#389e0d" size="large" type="success" @click="getCrop" :icon="Scissor" style="font-size: 18px;">裁 剪</el-button>
      </div>
    </template>
  </el-dialog>
</template>
<script setup>
import 'vue-cropper/dist/index.css';
import { VueCropper } from 'vue-cropper';
import { ElMessage } from 'element-plus';
import { Close, Scissor } from '@element-plus/icons-vue';
import { urlToFile } from '@/tools';
import {
  ref,
  reactive,
  nextTick,
  defineExpose,
  defineEmits,
  defineProps,
} from 'vue';

const emit = defineEmits(['onCropper']);
const props = defineProps(['options']);

const isShow = ref(false);
const cropper = ref(null);
const cropBox = ref(null);

let currentFile = null;
let options = reactive({
  img: '', // 原图文件
  autoCrop: true, // 默认生成截图框
  fixedBox: false, // 固定截图框大小
  canMoveBox: true, // 截图框可以拖动
  autoCropWidth: 200, // 截图框宽度
  autoCropHeight: 200, // 截图框高度
  fixed: true, // 截图框宽高固定比例
  fixedNumber: [1, 1], // 截图框的宽高比例
  centerBox: true, // 截图框被限制在图片里面
  canMove: true, // 上传图片不允许拖动
  canScale: true, // 上传图片不允许滚轮缩放
  enlarge: 1, // 图片根据截图框输出比例倍数
  full: true, // 是否输出原图比例的截图
  maxImgSize: 6000, // 限制图片最大宽度和高度
});

// 自定义尺寸
const onChange = (val) => {
  if (!options.fixed) {
    ElMessage.warning({
      dangerouslyUseHTMLString: true,
      offset: 80,
      message:
        '<strong style="color: #555;">请将 <i style="color:#c2232a;">固定比例</i> 设置为 <i style="color:#c2232a;">是</i> </strong>',
    });
    return;
  }
  options.autoCropWidth++;
};

// 显示
const onShow = (file) => {
  currentFile = file;
  for (let key in props.options) {
    if (key == 'fixedNumber') {
      let arr = [];
      arr.push(props.options[key].split(',')[0] * 1);
      arr.push(props.options[key].split(',')[1] * 1);
      options[key] = arr;
    } else {
      options[key] = props.options[key];
    }
  }
  isShow.value = true;
  // 根据原图比例展示
  //   const img = new Image();

  //   img.onload = function () {
  //     let imgWidth = img.width;
  //     let imgHeight = img.height;
  //     let ratio = imgHeight / imgWidth;
  //     nextTick(() => {
  //       // 当元素被渲染后
  //       let boxWidth = cropBox.value.offsetWidth;
  //       let boxHeight = parseInt(boxWidth * ratio); // 计算出元素的高度
  //       cropBox.value.style.height = boxHeight + 'px';
  //     });
  //   };
  //   img.src = file.url;

  // 读取原图
  let reader = new FileReader();

  if (!file.raw || !file.raw instanceof Blob) {
    // 处理网络图片
    urlToFile(file.url, (res) => {
      reader.readAsDataURL(res);
      reader.onload = (e) => {
        options.img = e.target.result;
      };
    });
  } else {
    reader.readAsDataURL(file.raw);
    reader.onload = (e) => {
      options.img = e.target.result; // base64
    };
  }
};

// 获取截图信息
const getCrop = () => {
  // 获取截图的 base64 数据
  //   cropper.value.getCropData((data) => {
  //     closeDialog();
  //   });
  cropper.value.getCropBlob((blob) => {
    // console.log(blob);
    let file = new File([blob], currentFile.name, {
      type: blob.type,
      lastModified: Date.now(),
    });

    let result = {
      index: currentFile.uid,
      file: file,
    };
    emit('onCropper', result);
    isShow.value = false;
  });
};

// 关闭弹框
const closeDialog = () => {
  // 初始化参数
  options = undefined;
  options = reactive({
    img: '', // 原图文件
    autoCrop: true, // 默认生成截图框
    fixedBox: false, // 固定截图框大小
    canMoveBox: true, // 截图框可以拖动
    autoCropWidth: 200, // 截图框宽度
    autoCropHeight: 200, // 截图框高度
    fixed: true, // 截图框宽高固定比例
    fixedNumber: [1, 1], // 截图框的宽高比例
    centerBox: true, // 截图框被限制在图片里面
    canMove: true, // 上传图片不允许拖动
    canScale: true, // 上传图片不允许滚轮缩放
    enlarge: 1, // 图片根据截图框输出比例倍数
    full: true, // 是否输出原图比例的截图
    maxImgSize: 6000, // 限制图片最大宽度和高度
  });
  currentFile = null;
};
defineExpose({ onShow });
</script>
<style lang='scss' scoped>
.dr-label {
  margin-left: 30px;
  margin-right: 10px;
}
.avatar-crop {
  width: 100%;
  height: calc(100vh - 160px);
  position: relative;
  .crop-box {
    border-radius: 4px;
    overflow: hidden;
  }
}
</style>