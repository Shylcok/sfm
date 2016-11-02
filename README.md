
##1.接口说明	
-	1.接口分需要用户权限和不需要权限，需要用户权限的登录取得有效cookie后才能访问，
-	2.为了防止cookie篡改攻击，cookie设置了加密和httponly，js不能访问 
-	3.为了防止跨站攻击，会开启xsrf验证，前端与需要如下（验证目前关闭了）

		jQuery.postJSON = function(url, data, callback) {
		    data._xsrf = getCookie("_xsrf");
		    jQuery.ajax({
		        url: url,
		        data: jQuery.param(data),
		        dataType: "json",
		        type: "POST",
		        success: callback
		    });
		}
-	4.部分非敏感的信息，例如用户昵称会放在cookie，提供给js
-	5.host:139.224.44.238:13910
-	6.返回结果格式如下，code＝0表示接口正常返回，msg附带接口返回说明，data为接口返回数据
		
		{
		"msg": "用户名或者密码不匹配",
		"status_code": 200,
		"code": 112,
		"data":{}
		}
-	7.接口自带权限登记
		
		T: 游客权限
		U: 用户权限
-	8.前端调试需要设置host，便于跨子域名设置cookie

		vi /etc/hosts   (mac)
		127.0.0.1       www.sfm.com
		139.224.44.238  api.sfm.com

##2.返回状态说明
	状态码									含义
	200 OK								GET请求成功
	202 ACCEPTED						POST请求成功
	401 FORBIDDEN						token无效,被禁止访问
	400 BAD REQUEST						POST请求失败或GET请求参数有误
	403 FORBIDDEN						token无效,被禁止访问
	404 NOT FOUND						请求的资源不存在，路由出差
	500 INTERNAL SERVER ERROR			内部错误
	

###用户中心接口列表

####1.登录
	/api/user/signin
-	【权限】T
-	【说明】

	>登录后获取加密user_token,存在cookie12小时   
	>登录后用户名放在cookie中12小时   	
	>
			user_name="sfm _user"
			
-	【参数】

		{
		  "mobile_uer_name": "13636672380",
		  "pwd":"124"
		}

####2.注册
	/api/user/signup	
-	【权限】T
-	【说明】
-	【参数】

		{
		  "mobile": "1331310",
		  "pwd":"12345",
		  "sms_verify": "111"
		}

####3.发送验证码
	/api/user/send_verify_code
-	【权限】T
-	【说明】

	>后台有效时间300s
-	【参数】
	
		{
		  "mobile": "13636672480"
		}

####4.注销
	/api/user/logout
-	【权限】U
-	【说明】

	> 清楚cookie

####5.修改密码
	/api/user/modify_pwd
-	【权限】U
-	【参数】

		{
		  "mobile": "1332122310",
		  "old_pwd":"123425",
		  "new_pwd": "11"
		}

####6.修改用户名
	/api/user/modify_user_name
-	【权限】U
-	【参数】

		{
		  "new_user_name":"suyuan"
		}

####7.获取用户信息
	/api/user/get_user_info
-	【权限】U


###订单系统接口列表

####1.获取收货地址
	/api/order/get_address
-	【权限】U
-	【说明】

	>登录后获取该用户下的所有收货地址，不需要参数
-	【参数】

####2.添加收货地址
	/api/order/add_address
-	【权限】U
-	【说明】

	>is_default 为1表示默认地址，0表示非默认地址
-	【参数】

		{
		  "address_info": {
		    "name": "suyuan",
		    "mobile": "13636672480",
		    "address": "江苏省扬州市",
		    "is_default": 1
		  }
		}

		
####3.更新收货地址
	/api/order/update_address
-	【权限】U
-	【说明】

	>id为收货地址的主键id
-	【参数】

		{
		  "id":1,
		  "address_info": {
		    "name": "suyuan",
		    "mobile": "13636672480",
		    "address": "江苏省扬州市1",
		    "is_default": 1
		  }
		}
		
####4.删除收货地址
	/api/order/delete_address
-	【权限】U
-	【说明】

	>id为收货地址的主键id
-	【参数】

		{
		  "id":1
		}
		
####5.设置默认收货地址
	/api/order/set_default
-	【权限】U
-	【说明】

	>id为收货地址的主键id
-	【参数】

		{
		  "id":1
		}

###购物车接口列表

####1.添加购物车
	/api/cart/add_cart
-	【权限】U
-	【说明】

	> 该接口用于详情页添加到购物车使用, sku_inc_count 是增量，一般为1
- 	【参数】

		{
		  "sku_id":"1",
		  "sku_inc_count":1
		}
		
####2.计算购物车sku数量
	/api/cart/cart_count
-	【权限】U
-	【说明】
- 	【参数】

####3.购物车列表
	/api/cart/cart_list
-	【权限】U
-	【说明】
- 	【参数】		

####4.更新购物车
	/api/cart/update_cart
-	【权限】U
-	【说明】
	
	>该功能和添加购物车不矛盾，sku_cout 是更新后的结果数量
- 	【参数】

		{
		  "sku_id":"1",
		  "sku_count":1
		}
		
####5.删除购物车
	/api/cart/del_cart
-	【权限】U
-	【说明】
	
	>该功能和更新购物车有点重复，更新购物车中 sku_count=0 也为删除 
- 	【参数】

		{
		  "sku_id":"1",
		  "sku_count":1
		}
		
###订单接口列表

####1.准备订单
	/api/order/prepare_order
-	【权限】U
-	【说明】
- 	【参数】

		{
		  "order_type": "cart", 
		  "cart_list": [
		  					{'cart_id':'2'},
		  					{'cart_id':'18'],
		  "sku_list": [
		  				{'sku_id':'ad561','sku_count':1},
		  				{'sku_id':'ad521','sku_count':1},
		  				 ],
		  "counpon_code": ""
		}
	
	> order_type:"cart"从购物车到达，cart_list中为cart_id列表 或者"sku"从商详到达，sku_list为sku列表
	
	
	
	
	