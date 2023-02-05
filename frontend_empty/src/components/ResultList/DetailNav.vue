<template>
	<div class="detail-nav">
		<div class="logo">
			NKU
		</div>
		<div class="search">
			<search-box-detail></search-box-detail>
		</div>
		<div class="right">
			<img
				v-if="store.state.UserProfile != ''"
				class="ava"
				:src="avator"
				alt=""
				@click="gotouser"
			/>
			<div class="link" v-else>
				<router-link class="btn1" :to="{ path: '/login' }">登录</router-link>|
				<router-link class="btn2" :to="{ path: '/register' }">注册</router-link>
			</div>
		</div>
	</div>
</template>
<script>
import SearchBoxDetail from "@/components/ResultList/SearchBoxDetail.vue";

export default {
	components: {
		SearchBoxDetail,
	},
};
</script>
<script setup>
import { getIP } from "@/api/index.js";
import store from "@/store/index.js";
import { useRouter } from "vue-router";

const router = useRouter();
const avator = getIP() + store.state.UserProfile.avator || "";
function gotouser() {
	router.push({ path: "/userprofile" });
}

</script>

<style lang="less" scoped>
.detail-nav {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 0.1rem 0.15rem 0.15rem 0.2rem;
	border-bottom: 1px solid rgba(156, 6, 250, 0.247);
	position: sticky;
	position: -webkit-sticky; // 兼容 -webkit 内核的浏览器
	top: 0px;
	background-color: rgba(156, 6, 250, 0.247);
	.logo {
		font-size: 0.3rem;
		font-weight: 900;
		position: relative;
	}
	.search {
		position: absolute;
		top: 0.1rem;
		left: 1rem;
	}
	.right {
		display: flex;
		justify-content: space-around;
		align-items: center;
		.icon {
			width: 0.25rem;
			height: 0.25rem;
			fill: #222;
			margin-right: 0.2rem;
		}
		.ava {
			height: 0.4rem;
			height: 0.4rem;
			border-radius: 0.4rem;
			cursor: pointer;
		}
		.btn1 {
			font-size: 0.15rem;
			margin-right: 0.05rem;
			font-weight: 900;
		}
		.btn2 {
			font-size: 0.15rem;
			margin-left: 0.05rem;
			font-weight: 900;
		}
	}
}
</style>
