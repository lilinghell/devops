<template>
  <q-layout view="lHr LpR lfr">
    <div class="container column">
      <div class="col row">
        <div class="col-6 full-height text-left">
          <q-img
            :src="require(`@/assets/thecopenhagencatalog-ebook/${cover}`)"
            class="full-height"
          />
        </div>
        <div class="col-6 row flex-center relative-position">
          <div class="login-wrapper">
            <Authorized
              :authority="$route.meta.authority"
              :noMatch="$route.meta.noMatch"
            >
              <router-view />
            </Authorized>
          </div>
          <q-footer class="bg-transparent">
            <Footer />
          </q-footer>
        </div>
      </div>
    </div>
  </q-layout>
</template>

<script>
import Footer from './Footer';
import Authorized from '@/components/Authorized';
export default {
  name: 'LoginLayout',
  components: { Authorized, Footer },
  data() {
    return {
      covers: [
        'thecopenhagencatalog-ebook-3.png',
        'thecopenhagencatalog-ebook-4.png',
        'thecopenhagencatalog-ebook-5.png',
        'thecopenhagencatalog-ebook-6.png',
        'thecopenhagencatalog-ebook-7.png',
        'thecopenhagencatalog-ebook-8.png',
        'thecopenhagencatalog-ebook-9.png',
        'thecopenhagencatalog-ebook-10.png',
        'thecopenhagencatalog-ebook-11.png',
        'thecopenhagencatalog-ebook-12.png',
        'thecopenhagencatalog-ebook-13.png',
        'thecopenhagencatalog-ebook-14.png',
        'thecopenhagencatalog-ebook-15.png',
        'thecopenhagencatalog-ebook-16.png',
        'thecopenhagencatalog-ebook-17.png',
        'thecopenhagencatalog-ebook-18.png',
        'thecopenhagencatalog-ebook-19.png',
        'thecopenhagencatalog-ebook-20.png',
        'thecopenhagencatalog-ebook-21.png',
        'thecopenhagencatalog-ebook-22.png',
        'thecopenhagencatalog-ebook-23.png',
        'thecopenhagencatalog-ebook-24.png',
        'thecopenhagencatalog-ebook-25.png',
        'thecopenhagencatalog-ebook-26.png',
        'thecopenhagencatalog-ebook-27.png',
        'thecopenhagencatalog-ebook-28.png',
        'thecopenhagencatalog-ebook-29.png',
        'thecopenhagencatalog-ebook-30.png',
        'thecopenhagencatalog-ebook-31.png',
        'thecopenhagencatalog-ebook-32.png',
        'thecopenhagencatalog-ebook-33.png',
        'thecopenhagencatalog-ebook-34.png',
        'thecopenhagencatalog-ebook-35.png',
        'thecopenhagencatalog-ebook-36.png',
        'thecopenhagencatalog-ebook-37.png',
        'thecopenhagencatalog-ebook-38.png',
        'thecopenhagencatalog-ebook-39.png',
        'thecopenhagencatalog-ebook-40.png',
        'thecopenhagencatalog-ebook-41.png',
        'thecopenhagencatalog-ebook-42.png',
        'thecopenhagencatalog-ebook-43.png',
        'thecopenhagencatalog-ebook-44.png',
        'thecopenhagencatalog-ebook-45.png',
        'thecopenhagencatalog-ebook-46.png',
        'thecopenhagencatalog-ebook-47.png',
        'thecopenhagencatalog-ebook-48.png',
        'thecopenhagencatalog-ebook-49.png',
        'thecopenhagencatalog-ebook-50.png',
        'thecopenhagencatalog-ebook-51.png',
        'thecopenhagencatalog-ebook-52.png',
        'thecopenhagencatalog-ebook-53.png',
        'thecopenhagencatalog-ebook-54.png',
        'thecopenhagencatalog-ebook-55.png',
        'thecopenhagencatalog-ebook-56.png',
        'thecopenhagencatalog-ebook-57.png',
        'thecopenhagencatalog-ebook-58.png',
        'thecopenhagencatalog-ebook-59.png',
        'thecopenhagencatalog-ebook-60.png',
        'thecopenhagencatalog-ebook-61.png',
        'thecopenhagencatalog-ebook-62.png',
        'thecopenhagencatalog-ebook-63.png',
        'thecopenhagencatalog-ebook-64.png',
        'thecopenhagencatalog-ebook-66.png',
        'thecopenhagencatalog-ebook-67.png',
        'thecopenhagencatalog-ebook-68.png',
        'thecopenhagencatalog-ebook-69.png',
        'thecopenhagencatalog-ebook-70.png',
        'thecopenhagencatalog-ebook-71.png',
        'thecopenhagencatalog-ebook-74.png',
        'thecopenhagencatalog-ebook-75.png',
        'thecopenhagencatalog-ebook-76.png',
        'thecopenhagencatalog-ebook-77.png',
        'thecopenhagencatalog-ebook-78.png',
        'thecopenhagencatalog-ebook-79.png',
        'thecopenhagencatalog-ebook-80.png',
        'thecopenhagencatalog-ebook-81.png',
        'thecopenhagencatalog-ebook-82.png',
        'thecopenhagencatalog-ebook-83.png',
        'thecopenhagencatalog-ebook-84.png',
        'thecopenhagencatalog-ebook-85.png',
        'thecopenhagencatalog-ebook-86.png',
        'thecopenhagencatalog-ebook-87.png',
        'thecopenhagencatalog-ebook-88.png',
        'thecopenhagencatalog-ebook-89.png',
        'thecopenhagencatalog-ebook-90.png',
        'thecopenhagencatalog-ebook-91.png',
        'thecopenhagencatalog-ebook-92.png',
        'thecopenhagencatalog-ebook-93.png',
        'thecopenhagencatalog-ebook-94.png',
        'thecopenhagencatalog-ebook-95.png',
        'thecopenhagencatalog-ebook-96.png',
        'thecopenhagencatalog-ebook-97.png',
        'thecopenhagencatalog-ebook-98.png',
        'thecopenhagencatalog-ebook-99.png',
        'thecopenhagencatalog-ebook-100.png',
        'thecopenhagencatalog-ebook-101.png',
        'thecopenhagencatalog-ebook-102.png',
        'thecopenhagencatalog-ebook-103.png',
        'thecopenhagencatalog-ebook-104.png',
        'thecopenhagencatalog-ebook-105.png',
        'thecopenhagencatalog-ebook-106.png',
        'thecopenhagencatalog-ebook-108.png',
        'thecopenhagencatalog-ebook-109.png',
        'thecopenhagencatalog-ebook-110.png',
        'thecopenhagencatalog-ebook-111.png',
        'thecopenhagencatalog-ebook-112.png',
        'thecopenhagencatalog-ebook-113.png',
        'thecopenhagencatalog-ebook-114.png',
        'thecopenhagencatalog-ebook-115.png',
        'thecopenhagencatalog-ebook-116.png',
        'thecopenhagencatalog-ebook-117.png',
        'thecopenhagencatalog-ebook-118.png',
        'thecopenhagencatalog-ebook-119.png',
        'thecopenhagencatalog-ebook-120.png',
        'thecopenhagencatalog-ebook-121.png',
        'thecopenhagencatalog-ebook-122.png',
        'thecopenhagencatalog-ebook-123.png',
        'thecopenhagencatalog-ebook-124.png',
        'thecopenhagencatalog-ebook-125.png',
        'thecopenhagencatalog-ebook-126.png',
        'thecopenhagencatalog-ebook-127.png',
        'thecopenhagencatalog-ebook-128.png',
        'thecopenhagencatalog-ebook-129.png',
        'thecopenhagencatalog-ebook-130.png',
        'thecopenhagencatalog-ebook-131.png',
        'thecopenhagencatalog-ebook-132.png',
        'thecopenhagencatalog-ebook-133.png',
        'thecopenhagencatalog-ebook-134.png',
        'thecopenhagencatalog-ebook-135.png',
        'thecopenhagencatalog-ebook-136.png',
        'thecopenhagencatalog-ebook-137.png',
        'thecopenhagencatalog-ebook-138.png',
        'thecopenhagencatalog-ebook-139.png',
        'thecopenhagencatalog-ebook-140.png',
        'thecopenhagencatalog-ebook-141.png'
      ],
      randomIndex: Math.random(),
      timeout: 0
    };
  },
  computed: {
    cover() {
      return this.covers[Math.floor(this.randomIndex * this.covers.length)];
    }
  },
  methods: {},
  created() {
    this.timeout = setInterval(() => {
      this.randomIndex = Math.random();
    }, 10000);
  },
  mounted() {},
  destroyed() {
    clearTimeout(this.timeout);
  }
};
</script>

<style lang="stylus" scoped>

.container
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: white;
.login-wrapper
  padding: 20px 0;
  margin-bottom: 40px;
  position: relative;
  width: 100%
.logo
  width: 200px;
  display: block;
  margin: 0 auto 20px;
</style>
