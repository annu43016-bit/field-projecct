const form=document.getElementById('predictionForm');
const emptyState=document.getElementById('emptyState');
const resultContent=document.getElementById('resultContent');
const submitBtn=document.getElementById('submitBtn');
const descriptions={
  "Normal thyroid pattern":"The model classified these measurements in the dataset's normal class.",
  "Hyperthyroid pattern":"The model classified these measurements in the dataset's hyperthyroid class.",
  "Hypothyroid pattern":"The model classified these measurements in the dataset's hypothyroid class."
};
form.addEventListener('submit',async(e)=>{
  e.preventDefault();
  const keys=['t3_resin','total_thyroxin','total_triiodothyronine','basal_tsh','max_tsh_difference'];
  const payload={}; keys.forEach(k=>payload[k]=document.getElementById(k).value);
  submitBtn.disabled=true;submitBtn.innerHTML='Analyzing values <span>◌</span>';
  try{
    const response=await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const data=await response.json();
    if(!response.ok) throw new Error(data.error||'Unable to analyze values.');
    emptyState.classList.add('hidden');resultContent.classList.remove('hidden');
    document.getElementById('predictionTitle').textContent=data.prediction;
    document.getElementById('predictionDescription').textContent=descriptions[data.prediction]||'Educational model output.';
    document.getElementById('confidenceValue').textContent=data.confidence+'%';
    document.getElementById('confidenceBar').style.width=data.confidence+'%';
    const list=document.getElementById('probabilityList');list.innerHTML='';
    Object.entries(data.scores).sort((a,b)=>b[1]-a[1]).forEach(([name,value])=>{
      const item=document.createElement('div');item.className='prob-item';
      const label=document.createElement('span');label.textContent=name;
      const score=document.createElement('b');score.textContent=value+'%';
      const track=document.createElement('div');track.className='prob-track';
      const fill=document.createElement('i');fill.style.width=value+'%';track.appendChild(fill);
      item.append(label,score,track);list.appendChild(item);
    });
  }catch(err){alert(err.message)}
  finally{submitBtn.disabled=false;submitBtn.innerHTML='Analyze lab values <span>✦</span>'}
});
document.getElementById('sampleBtn').addEventListener('click',()=>{
  document.getElementById('t3_resin').value=110;
  document.getElementById('total_thyroxin').value=9.5;
  document.getElementById('total_triiodothyronine').value=1.8;
  document.getElementById('basal_tsh').value=1.2;
  document.getElementById('max_tsh_difference').value=2.0;
  emptyState.classList.remove('hidden');resultContent.classList.add('hidden');
});
