(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[12],{e498:function(e,a,t){"use strict";t.r(a);var l=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("q-page",{staticClass:"flex justify-center"},[t("div",{staticClass:"work-area"},[t("div",{staticClass:"manager-header"},[t("div",{staticClass:"text-h3"},[e._v("\n        受访者管理\n      ")]),t("q-separator",{attrs:{color:"black"}}),t("div",{staticClass:"main-btn-group"},[t("q-btn",{attrs:{flat:"",color:"primary","icon-right":"arrow_forward"}},[e._v("\n          导入受访者列表\n        ")])],1)],1),t("div",{staticClass:"q-pa-md"},[t("q-table",{attrs:{title:"受访者",data:e.data,columns:e.columns,"row-key":"name","selected-rows-label":e.getSelectedString,selection:"multiple",selected:e.selected},on:{"update:selected":function(a){e.selected=a}}})],1),t("q-uploader",{attrs:{url:"http://192.168.236.95:8000/app_01/receivefile/",accept:".xls,.xlsx","max-files":"1"}})],1)])},s=[],n={name:"Respondents",data(){return{selected:[],columns:[{name:"id",required:!0,label:"学号/工号",align:"left",field:"id",sortable:!0},{name:"name",label:"姓名",field:"name",sortable:!0},{name:"fat",label:"学校",field:"school",sortable:!0},{name:"carbs",label:"学院",field:"major"},{name:"protein",label:"性别",field:"protein"},{name:"sodium",label:"手机号",field:"sodium"},{name:"sodium",label:"邮箱",field:"sodium"}],data:[{}]}},methods:{getSelectedString(){return 0===this.selected.length?"":`${this.selected.length} record${this.selected.length>1?"s":""} selected of ${this.data.length}`}}},r=n,i=t("2877"),d=t("9989"),o=t("eb85"),c=t("9c40"),m=t("eaac"),u=t("ee89"),p=t("eebe"),b=t.n(p),f=Object(i["a"])(r,l,s,!1,null,"3dd7fa99",null);a["default"]=f.exports;b()(f,"components",{QPage:d["a"],QSeparator:o["a"],QBtn:c["a"],QTable:m["a"],QUploader:u["a"]})}}]);