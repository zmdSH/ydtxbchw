const app = getApp();
Page({
  data: {
    inputValue: '', // 输入的文字内容
    imagePath: '', // 拍摄的照片路径
    receivedTexts: '',//获取输入的文字
    imageUrl: '',//读取的图片路径
    imagepath2: ''//图片路径
  },

  // 输入文字内容
  bindInput(e) {
    this.setData({
      inputValue: e.detail.value
    })
  },

  // 拍摄照片
  takePhoto() {
    var that = this;
    wx.chooseImage({
      count: 1,
      sourceType: ['camera', 'album'],
      success(res) {
        const tempFilePath = res.tempFilePaths[0];
        const tempFilePath2 = res.tempFilePaths[0];
            
         wx.getFileSystemManager().readFile({
          filePath: tempFilePath,
          encoding: 'base64',
          success(data) {
            const base64 = data.data;
            const fileFormat = tempFilePath.substring(tempFilePath.lastIndexOf(".") + 1, tempFilePath.length);
            that.setData({
              imagePath: `data:image/${fileFormat};base64,${base64}`,
           imagepath2: tempFilePath   }, function() { console.log("image2",that.data.imagepath2);
                                  });                  
                                },
          fail(error) {
            console.log(error);
          }
        });
      }
    })
  },
  
 
  receivetexts()  {
      var that = this;
      // 发起请求获取后端保存的文字
      wx.request({
        url:  `${app.globalData.serverUrl}/texts`,
        method: 'GET',
        success: function(res) {
          // 将接收到的文字保存到 receivedTexts 变量
          that.setData({
            receivedTexts: res.data.texts.join('\n')
          });
        },
        fail: function(res) {
          console.log('Request failed: ', res);
        }
      });
      },  
      receiveimg()  {
        // 发起请求获取后端保存的文字
        wx.request({
          url:  `${app.globalData.serverUrl}/get/image`,
          method: 'GET',
          responseType: 'arraybuffer',
          success: res => {
            // 将接收到的图片数据转为 base64 格式
            const base64 = wx.arrayBufferToBase64(res.data);
    
            // 更新图片路径，用于在前端页面显示
            this.setData({
              imageUrl: 'data:image/jpeg;base64,' + base64
            });
          },
          fail: res => {
            console.log('Request failed: ', res);
          }
        });
        },  
  // 提交数据到服务器
  submitData() {
    var that = this;    
    const { inputValue, imagePath ,imagePath2,receivedTexts, imageUrl } = this.data;    
    // 上传文字内容
    
    wx.request({
      url: `${app.globalData.serverUrl}/receive/text`,
      method: 'POST',
      data: {
        text: inputValue
      },
      success(res) {
        // 处理上传成功的逻辑
        console.log('文字上传成功', res.data);
      },
      fail(err) {
        // 处理上传失败的逻辑
        console.log('文字上传失败', err);
      }
    });

    // 上传图片
    wx.uploadFile({
      url: `${app.globalData.serverUrl}/receive/img`,
      filePath: that.data.imagepath2,
      name: 'image',
               success(res) {
        // 处理上传成功的逻辑
        console.log('图片上传成功', res.data);
      },
      fail(err) {
        // 处理上传失败的逻辑
        console.log('图片上传失败', err);
        console.log('图片上传失败', that.data.imagepath2);
        console.log('图片上传失败', imagepath2);
      }
    });
  }
})
