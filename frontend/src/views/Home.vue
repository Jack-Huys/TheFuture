<template>
  <div class="home">
    <div class="hero">
      <h1>未来</h1>
      <p class="subtitle">张雪峰视角的人生规划咨询平台</p>
      <p class="quote">"社会就是一个大筛子，用学历筛孩子，用房子筛父母，用工作筛家庭。"</p>
      <p class="desc">高考志愿 · 考研择校 · 职业规划 · 人生理想</p>
      <button class="start-btn" @click="goConsult">开始咨询</button>
    </div>

    <div class="features">
      <div class="feature">
        <h3>🗣️ 张雪峰风格</h3>
        <p>东北大哥语气，直接给答案，不说废话，敢说真话不怕得罪人</p>
      </div>
      <div class="feature">
        <h3>📊 数据驱动</h3>
        <p>不看理想看现实，就业率、薪资才是真，用数据说话</p>
      </div>
      <div class="feature">
        <h3>🎯 精准定位</h3>
        <p>灵魂追问，搞清楚你的情况再给建议，不拍脑袋</p>
      </div>
    </div>

    <div class="scope">
      <h2>我们能帮你</h2>
      <div class="scope-list">
        <div class="scope-item">
          <span class="scope-icon">🎓</span>
          <h3>高考志愿</h3>
          <p>选学校、选专业、志愿填报策略</p>
        </div>
        <div class="scope-item">
          <span class="scope-icon">📚</span>
          <h3>考研择校</h3>
          <p>院校性价比、专业选择、备考规划</p>
        </div>
        <div class="scope-item">
          <span class="scope-icon">💼</span>
          <h3>职业规划</h3>
          <p>就业方向、行业前景、职业发展路径</p>
        </div>
        <div class="scope-item">
          <span class="scope-icon">🌟</span>
          <h3>人生理想</h3>
          <p>阶层流动、人生选择、现实与理想平衡</p>
        </div>
      </div>
    </div>

    <div class="examples">
      <h2>你可以问</h2>
      <div class="example-list">
        <div class="example" @click="ask('我孩子560分河南，想学金融')">
          "我孩子560分河南，想学金融"
        </div>
        <div class="example" @click="ask('计算机和电子信息哪个更有前景')">
          "计算机和电子信息哪个更有前景"
        </div>
        <div class="example" @click="ask('双非考研到985值得吗')">
          "双非考研到985值得吗"
        </div>
        <div class="example" @click="ask('普通家庭的孩子学什么专业好')">
          "普通家庭的孩子学什么专业好"
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goConsult = () => {
  router.push('/consult')
}

const ask = (question) => {
  router.push({ path: '/consult', query: { q: question } })
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero {
  text-align: center;
  padding: 60px 20px;
}

.hero h1 {
  font-size: 72px;
  margin: 0;
  font-weight: 700;
}

.subtitle {
  font-size: 28px;
  margin: 20px 0 10px;
  opacity: 0.95;
}

.quote {
  font-size: 18px;
  margin: 20px auto;
  max-width: 600px;
  padding: 20px 30px;
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  font-style: italic;
  line-height: 1.6;
}

.desc {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 40px;
  letter-spacing: 2px;
}

.start-btn {
  background: white;
  color: #667eea;
  border: none;
  padding: 16px 48px;
  font-size: 20px;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.features {
  display: flex;
  justify-content: center;
  gap: 40px;
  padding: 60px 20px;
  flex-wrap: wrap;
}

.feature {
  background: rgba(255,255,255,0.1);
  padding: 30px;
  border-radius: 16px;
  width: 280px;
  text-align: center;
}

.feature h3 {
  font-size: 20px;
  margin: 0 0 10px;
}

.feature p {
  font-size: 14px;
  opacity: 0.85;
  margin: 0;
  line-height: 1.5;
}

.scope {
  text-align: center;
  padding: 60px 20px;
  background: rgba(0,0,0,0.1);
}

.scope h2 {
  font-size: 28px;
  margin-bottom: 40px;
}

.scope-list {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.scope-item {
  background: rgba(255,255,255,0.1);
  padding: 30px 25px;
  border-radius: 16px;
  width: 220px;
  text-align: center;
}

.scope-icon {
  font-size: 36px;
  display: block;
  margin-bottom: 15px;
}

.scope-item h3 {
  font-size: 18px;
  margin: 0 0 10px;
}

.scope-item p {
  font-size: 13px;
  opacity: 0.8;
  margin: 0;
  line-height: 1.4;
}

.examples {
  text-align: center;
  padding: 60px 20px;
}

.examples h2 {
  font-size: 24px;
  margin-bottom: 30px;
}

.example-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 500px;
  margin: 0 auto;
}

.example {
  background: rgba(255,255,255,0.15);
  padding: 16px 24px;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 15px;
}

.example:hover {
  background: rgba(255,255,255,0.25);
}
</style>
