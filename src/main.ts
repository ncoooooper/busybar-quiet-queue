import {surface,panel,label,mint,amber,report,type Frame} from "@shared/surface";
import {loadValues} from "@shared/settings";

type Queue={count:number;head:number;topic:string};
let state:Queue|null=null,url="",status="Set operator URL",notice="",showCount=false,online=false,busy=false,closed=false;
let timer:ReturnType<typeof setInterval>|undefined;
function draw():Frame{
 const headline=!url?"Setup":!online?"Offline":!state?.count?"All clear":showCount?state.count+" waiting":"Ticket "+state.head;
 return [label("category",state?.count&&online?"DESK QUEUE":"QUIET QUEUE",1,0,amber,"front","tiny"),
 label("head",headline,1,7,mint),...panel("QUIET QUEUE",[status,state?.count?"Next #"+state.head+" / "+state.count+" waiting":"No waiting tickets",
 state?.topic||"",notice,"Click: accept / Start: sync","Wheel: ticket or count"])];
}
async function sync(accept=false){
 if(closed||!url||busy)return;
 busy=true;
 try{
   if(accept&&online&&state?.head){
     const expected=state.head;
     const result=await fetch(url+"/accept",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({head:expected})});
     if(!result.ok&&result.status!==409)throw Error("HTTP "+result.status);
     notice=result.ok?"Accepted #"+expected:"Head already changed";
     console.log("accept",expected,result.status);
   }
   const response=await fetch(url+"/queue");if(!response.ok)throw Error("HTTP "+response.status);
   const q=await response.json() as Queue;
   if(!Number.isInteger(q.count)||q.count<0||!Number.isInteger(q.head)||q.head<0||Boolean(q.count)!==Boolean(q.head)||typeof q.topic!=="string")throw Error("Invalid queue");
   state=q;online=true;status="Connected to desk";console.log("queue",q.count,"head",q.head);
 }catch(e){online=false;status=state?"Offline / last sync":"Operator unreachable";console.log("queue offline",String(e));}
 finally{busy=false;if(!closed)refresh();}
}
const refresh=surface(draw,k=>{
 if(k==="ok")void sync(true);
 else if(k==="start")void sync();
 else if(k==="up"||k==="down")showCount=!showCount;
},()=>{closed=true;if(timer!==undefined)clearInterval(timer);});
void loadValues().then(v=>{
 if(closed)return;url=String(v?.bridge||"").trim().replace(/\/+$/,"");refresh();
 if(url){void sync();timer=setInterval(()=>void sync(),10000);}
}).catch(report);
