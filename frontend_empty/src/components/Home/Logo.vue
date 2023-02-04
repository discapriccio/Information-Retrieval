<template>
	<div class="logo">
		<div class="container">
			<img src="@/assets/logo.jpeg" alt="" />
			<div class="text">
				<div class="master">南开大学图书检索系统</div>
				<div class="slug">
					Nankai University Book Retrieval System
				</div>
			</div>
		</div>
	</div>
</template>

<style lang="less" scoped>
html {
				font-size: 30px;
			}

.logo {
	margin-top: 1.6rem;
	margin-bottom: 0.2rem;
	display: flex;
	.container {
		margin: auto;
		display: flex;
		img {
			height: 1rem;
			width: 1rem;
		}
		.text {
			.master {
				font-size: 0.5rem;
				font-weight: 900;
			}
			.slug {
				font-size: 0.2rem;
				height: 0.2rem;
				position: relative;
			}
		}
	}
}
</style>
