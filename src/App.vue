<template>
  <a-layout class="layout">
    <a-layout-header :style="{ position: 'fixed', zIndex: 1, width: '100%', color: 'white', fontSize: '16px' }">
      <div class="logo" />
      经典猫狗识别
    </a-layout-header>
    <a-layout-content :style="{ padding: '0 400px', marginTop: '80px' }">
      <a-card>
        <a-upload-dragger
          ref="up"
          name="file"
          :customRequest="upload"
          @drop="handleDrop"
          :disabled="loading"
        >
            <div v-if="loading">
              <p class="ant-upload-drag-icon">
                <loading-outlined />
              </p>
              <a-progress :percent="defaultPercent" />
              <p class="ant-upload-text">
                Serverless实例正在识别，TensorFlow加载时间会比较长，但是不会超过两分钟...
              </p>
            </div>
            <div v-else>
              <p class="ant-upload-drag-icon">
                <inbox-outlined />
              </p>
              <p class="ant-upload-text">
                点击或拖动图片到这个区域
              </p>
            </div>
        </a-upload-dragger>
        <a-space v-if="imageUrl" class="result" direction="vertical">
          <a-card title="原图" >
            <template #extra>
              <a-button>
                保存
              </a-button>
            </template>
            <img :src="imageUrl" alt="" style="max-height: 200px">
          </a-card>
          <a-card :title="`它是${result}，这个结果正确吗?`" style="width: 100%" v-if="result!=''">
            <a-space>
              <a-button :loading="loading2" :disabled="disabled" @click="label(true)" type="primary" >正确</a-button>
              <a-button :loading="loading2" :disabled="disabled" @click="label(false)" type="error">错误</a-button>
            </a-space>
            <a-button></a-button>
          </a-card>
        </a-space>
      </a-card>
    </a-layout-content>
    <a-layout-footer :style="{ textAlign: 'center' }">
      xinwuyun ©2022 Powerd by serverless and animeGAN2 
    </a-layout-footer>
  </a-layout>
</template>

<script>
import { InboxOutlined,LoadingOutlined } from "@ant-design/icons-vue";
import { message } from "ant-design-vue";
import { defineComponent, ref } from "vue";


export default defineComponent({
  components: {
    InboxOutlined, LoadingOutlined
  },
  setup() {
    const up = ref(null);
    const imageUrl = ref('');
    const defaultPercent = ref(0);
    const result = ref('');    
    const loading = ref(false)
    const loading2 = ref(false)
    const disabled = ref(false)
    // function getBase64(img, callback) {
    //   const reader = new FileReader();
    //   reader.addEventListener('load', () => callback(reader.result));
    //   reader.readAsDataURL(img);
    // }

    const clear = () => {
      up.value = null;
      imageUrl.value = '';
      result.value = '';
      loading.value = false;
      disabled.value = false;
    }
    const upload = async (option) => {
      clear();
      loading.value = true;
      imageUrl.value = ""
      const reader = new FileReader();
      let file = option.file;
      
      reader.readAsDataURL(file);
      reader.onloadend = function(e) {
        const base64 = e.target.result.toString().split(',')[1];
        imageUrl.value = `data:image/jpg;base64, ${base64}`;
        if (e && e.target && e.target.result) {
          var raw = JSON.stringify({
            "image": base64
          });

          var requestOptions = {
            method: 'POST',
            body: raw,
          };
          fetch("https://1893791694056142.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/cloud-homework/dog-vs-cat-predict/dog-vs-cat", requestOptions)
            .then(response => response.json())
            .then(res => {
              let {dog, cat, code} = res;
              dog = parseFloat(dog)
              cat = parseFloat(cat)
              console.log(dog)
              console.log(cat)
              if(code != "0"){
                message.error(`Failed to identify.`);
                up.value.abort();
                option.onError();
                return;
              }
              if(dog > cat){result.value = "狗" }
              else{
                result.value = "猫";
              }
              loading.value = false;
              message.success("识别成功");
              option.onSuccess();
            })
            .catch((error) => {
              message.error(`API error ${error}`);
              up.value.abort();
              option.onError();
            });
        }
      }
      return true;
    }
    const label = (isCorrect) => {
      loading2.value = true;
      let l ;
      if( result.value == "狗"){
        l = isCorrect?"dog":"cat";
      }else{
        l = isCorrect?"cat":"dog";
      }
      const base64 = (imageUrl.value.split(", "))[1];
      var raw = JSON.stringify({
        "image": base64,
        "label": l
      });

      var requestOptions = {
        method: 'POST',
        body: raw,
      };
      
      fetch("https://dog-vs-t-upload-cloud-homework-azkjfipaes.cn-hangzhou.fcapp.run/upload", requestOptions)
        .then(response => response.json())
        .then(res => {
          let {code} = res;
          if(code != 0){
            message.error("Failed to label this image.");
            return;
          }
          loading2.value = false;
          message.success("提交成功");
          disabled.value = true;
        })
        .catch((error) => {
          loading2.value = false;
          message.error(`API error ${error}`);
        });
    }
    return {
      title: "猫狗识别工具",
      up,
      imageUrl,
      defaultPercent,
      result,
      loading,
      loading2,
      upload,
      label,
      disabled,
      fileList: ref([]),
      handleDrop: (e) => {
        console.log(e);
      },
    };
  },
});
</script>

<style>
.layout {
  height: 100vh;
}
.layout .logo {
  width: 120px;
  height: 31px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px 24px 16px 0;
  float: left;
}
.site-layout .site-layout-background {
  background: #fff;
}

.result {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

[data-theme="dark"] .site-layout .site-layout-background {
  background: #141414;
}
</style>
