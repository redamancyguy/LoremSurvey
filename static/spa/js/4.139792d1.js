(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[4],{"4ec3":function(e,t,a){"use strict";a.d(t,"b",(function(){return n})),a.d(t,"a",(function(){return l}));var s=a("b775");const n=e=>Object(s["a"])({url:"//192.168.243.95:8000/question/answer",method:"post",data:e}),l=e=>Object(s["a"])({url:"//0.0.0.0:8000/user/login",method:"post",data:e})},"66d1":function(e,t,a){},b775:function(e,t,a){"use strict";(function(e){var s=a("bc3a"),n=a.n(s),l=a("2a19");const r=n.a.create({baseURL:e.env.VUE_APP_BASE_API,timeout:99999});r.defaults.withCredentials=!0,r.interceptors.request.use((e=>(e.data=JSON.stringify(e.data),console.log(e),e.headers={"Content-Type":"application/json"},e)),(e=>(l["a"].create({message:e.toString(),color:"negative",position:"top",timeout:1500,icon:"warning"}),e))),r.interceptors.response.use((e=>{if(0===e.data.code||"true"===e.headers.success)return console.log(e),e.data}),(e=>(l["a"].create({message:e.toString(),color:"negative",position:"top",timeout:1500,icon:"warning"}),console.log(e.toString()),e))),t["a"]=r}).call(this,a("4362"))},c660:function(e,t,a){"use strict";a("66d1")},e3ba:function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("q-page",{staticClass:"main-con"},[a("div",[a("div",{staticClass:"paper-header"},[a("div",{staticClass:"text-h4 text-center paper-title"},[e._v(e._s(e.surveyData.title))]),e.$route.params.token?a("div",{staticClass:"text-center paper-time"},[e._v("ID:"+e._s(e.$route.params.token))]):e._e(),a("br"),a("div",{staticClass:"text-center"},[e._v(e._s(e.surveyData.desc))])]),a("q-form",{ref:"surveyForm",staticClass:"column",attrs:{autocorrect:"off",autocapitalize:"off",autocomplete:"off",spellcheck:"false"},on:{"validation-error":e.validError,submit:e.submit}},[e._l(e.surveyData.problemSet,(function(t,s){return a("div",{key:s,staticClass:"ques-section"},[0===t.type?a("div",[a("div",{staticClass:"text-h6 ques-title-large"},[a("b",[e._v(e._s(e._f("formatIndex")(t.index))+" / ")]),a("span",[e._v(e._s(t.title))]),t.need?a("span",{staticClass:"text-red"},[e._v(" *")]):e._e()]),a("q-input",{attrs:{disable:1===e.submitted,placeholder:"请输入",dense:!0,filled:"",rules:[function(e){return!t.need||null!=e&&""!=e||"必填项"}]},model:{value:e.answer.problemSet[s].answer,callback:function(t){e.$set(e.answer.problemSet[s],"answer",t)},expression:"answer.problemSet[i].answer"}})],1):1===t.type?a("div",[a("div",{staticClass:"text-h6 ques-title"},[a("b",[e._v(e._s(e._f("formatIndex")(t.index))+" / ")]),a("span",[e._v(e._s(t.title))]),t.need?a("span",{staticClass:"text-red"},[e._v(" *")]):e._e()]),a("q-field",{attrs:{rules:[function(e){return!t.need||null!=e||"必填项"}],borderless:"",disable:1===e.submitted},scopedSlots:e._u([{key:"control",fn:function(){return[a("q-option-group",{attrs:{options:t.options,color:"primary",type:"radio"},model:{value:e.answer.problemSet[s].option,callback:function(t){e.$set(e.answer.problemSet[s],"option",t)},expression:"answer.problemSet[i].option"}})]},proxy:!0}],null,!0),model:{value:e.answer.problemSet[s].option,callback:function(t){e.$set(e.answer.problemSet[s],"option",t)},expression:"answer.problemSet[i].option"}})],1):e._e()])})),"1"===e.surveyData.isopen?a("q-btn",{staticClass:"flex-center submit-btn",attrs:{label:1===e.submitted?"提交成功":"提交",color:1===e.submitted?"secondary":"primary",type:"submit",disable:0!==e.submitted,loading:-1===e.submitted}}):a("q-btn",{staticClass:"submit-btn flex-center",attrs:{label:"问卷已停止收集",disable:"",flat:"",color:"secondary"}})],2)],1),a("br"),a("q-separator"),a("div",{staticClass:"paper-footer text-center"},[e._v("\n\n    Copyright © 2021 LoremIpsum Team\n    "),a("br"),e._v("\n    问卷系统由"),a("span",{staticClass:"no-wrap"},[e._v("LoremSurvey")]),e._v("提供\n    "),a("br"),a("a",{staticClass:"q-link",attrs:{href:"#"}},[e._v("意见反馈")])])],1)},n=[],l=a("2a19"),r=a("4ec3"),i={name:"survey",data(){return{surveyData:{title:"编程学习调研问卷",isopen:"1",desc:"沈阳航空航天大学 软件工程LoremIpsum Team 调查问卷",stime:"2021/4/1",etime:"2021/6/1",problemSet:[{index:1,type:1,title:"您目前的职业是?",need:"True",options:[{label:"在校学生",value:"1"},{label:"政府/机关干部/公务员",value:"2"},{label:"企业管理者（包括基层及中高层管理者）",value:"3"},{label:"普通职员（办公室 / 写字楼工作人员）",value:"4"},{label:"专业人员（如医生 / 律师 / 文体 / 记者 / 老师等）",value:"5"},{label:"普通工人（如工厂工人 / 体力劳动者等）",value:"6"},{label:"商业服务业职工（如销售人员 / 商店职员 / 服务员等）",value:"7"},{label:"个体经营者 / 承包商",value:"8"},{label:"自由职业者",value:"9"},{label:"农林牧渔劳动者",value:"10"},{label:"退休",value:"11"},{label:"暂无职业",value:"12"},{label:"others",value:"#"}]},{index:2,type:1,title:"您学习编程多久了?",need:"True",options:[{label:"不到3个月",value:"1"},{label:"3-6个月",value:"2"},{label:"6-12个月",value:"3"},{label:"1-3年以上",value:"4"},{label:"3年以上",value:"5"},{label:"others",value:"#"}]},{index:7,type:1,title:"您希望订阅我们的信息吗?",need:"False",options:[{label:"是",value:"True"},{label:"否",value:"False"},{label:"others",value:"#"}]},{index:3,type:0,title:"您如何学习编程?",need:"False"},{index:4,type:0,title:"您学习的方向是?",need:"True"},{index:5,type:0,title:"您为什么要学习编程?",need:"True"},{index:6,type:0,title:"您的联系方式?",need:"False"}]},answer:{sessionid:null,problemSet:[]},submitted:0,res:null,sessionId:null}},async created(){this.sessionId=this.$route.params.token,"1"!==this.surveyData.isopen&&(this.submitted=1),this.answer.sessionid=this.sessionId;for(let e=0;e<this.surveyData.problemSet.length;++e)1===this.surveyData.problemSet[e].type?this.answer.problemSet.push({index:e+1,option:null}):0===this.surveyData.problemSet[e].type&&this.answer.problemSet.push({index:e+1,answer:null})},filters:{formatIndex:function(e){return e<10?"0"+e:e}},methods:{submit(){this.submitted=-1,Object(r["b"])(this.answer).then((e=>{1===e.code?setTimeout((()=>{this.submitted=1}),1e3):this.submitted=0}))},validError(){l["a"].create({message:"存在未填项",color:"negative",position:"top",timeout:1500,icon:"warning"})}}},o=i,u=(a("c660"),a("2877")),c=a("9989"),p=a("0378"),d=a("27f9"),b=a("8572"),m=a("9f0a"),v=a("9c40"),f=a("eb85"),h=a("eebe"),y=a.n(h),_=Object(u["a"])(o,s,n,!1,null,"117fbc21",null);t["default"]=_.exports;y()(_,"components",{QPage:c["a"],QForm:p["a"],QInput:d["a"],QField:b["a"],QOptionGroup:m["a"],QBtn:v["a"],QSeparator:f["a"]})}}]);