<template>
	<div class="home">
		<sample-nav></sample-nav>
		<logo></logo>
		<search-box></search-box>
		<footer></footer>
	</div>
</template>

<script>
// @ is an alias to /src
import SampleNav from "@/components/Home/SampleNav.vue";
import Logo from "@/components/Home/Logo.vue";
import SearchBox from "@/components/Home/SearchBox.vue";


export default {
	name: "Home",
	components: {
		SampleNav,
		Logo,
		SearchBox
	},
};
</script>

<style lang="less" scoped>
.home {
}
</style>
