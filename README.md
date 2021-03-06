
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
	
##2.cookie管理

>	所有cookie的安全期为12小时
>	用户退出后清除所有cookie  
>  用户登录后保存的cookie如下:	
>		
	sfm_user_token	用户登录权限认证，js无法操作
	user_name		用户名
	
	
	

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
	/api/user/signout
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
	/api/user/modify_user_info
-	【权限】U
-	【参数】

		{
		  "new_user_name":"suyuan",
		  "sex": 1
		}

####7.获取用户信息
	/api/user/get_user_info
-	【权限】U

####8.请求认证
	/api/user/set_auth
-	【权限】U
- 	【说明】

	> 认证成功的话，cookie中会有认证标示auth_is_pass=1, 否则auth_is_pass=0标示认证不成功
-	【参数】

		{
		  "real_name": "suyuan",
		  "id_code":"123421115",
		  "id_card_up": "www",
		  "id_card_down": "wwwww"
		}




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
		  "sku_inc_count":1,
		  "first_price": 100
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
		  "sku_count":1,
		  "first_price": 100
		}
		
####5.删除购物车
	/api/cart/del_cart
-	【权限】U
-	【说明】
	
	>该功能和更新购物车有点重复，更新购物车中 sku_count=0 也为删除 
- 	【参数】

		{
		  "sku_ids":["1", "2"]
		}
		
###订单接口列表

>订单状态,state
	
		0	未支付订单，
		1	已付款代发货，
		2	已发货，
		3	已收货,订单确认,交易成功，
		4	订单取消，
		5	订单过期, 
		99	进入支付状态'

####1.准备订单
	/api/order/prepare_order
-	【权限】U
-	【说明】
- 	【参数】

		{
		    "order_type": "cart",
		    "cart_list": [
		        {
		            "cart_id": "2",
		            "first_price": 10000
		        },
		        {
		            "cart_id": "18",
		            "first_price": 20000
		        }
		    ],
		    "sku_list": [
		        {
		            "sku_id": "ad561",
		            "sku_count": 1,
		            "first_price": 10000
		        },
		        {
		            "sku_id": "ad521",
		            "sku_count": 1,
		            "first_price": 30000
		        }
		    ],
		    "coupon_code": ""
		}
	
	> 所有的价格都以分为单位
	> order_type:"cart" 表示从购物车到达，cart_list中为cart_id列表，或者"sku"表示从商详到达，sku_list 为sku列表
	
####2.提交订单
	/api/order/commit_order
-	【权限】U
-	【说明】

	>提交订单后，state＝0， 订单处于未支付状态

- 	【参数】
		
		{
		    "address_id": 1,
		    "user_note": "要正品",
		    "order_type": "cart",
		    "cart_list": [
		        {
		            "cart_id": 1,
		            "first_price": 10
		        },
		        {
		            "cart_id": 3,
		            "first_price": 20
		        }
		    ],
		    "sku_list": [
		        {
		            "sku_id": "2",
		            "sku_count": 1,
		            "first_price": 10
		        },
		        {
		            "sku_id": "1",
		            "sku_count": 1,
		            "first_price": 10
		        }
		    ],
		    "coupon_code": ""
		}
	
	> 参数和准备订单的参数类似

####3.订单列表
	/api/order/get_order_list
-	【权限】U
-	【说明】
- 	【参数】	
		
		{
			"order_type": "all",
			"page": 1,
			"count": 10
		}
	>order_type:
	
		all				全部订单
		need_pay   		代付款
		need_send	 	代发货		
		need_receive 	待收货
		complete		已完成
		cancel			已取消
		overtime		已过期

####4.支付页面订单简讯
	/api/order/get_order_brief_for_pay
-	【权限】U
-	【说明】
- 	【参数】	

		{
		  "order_id": "14784316383"
		}
		
####5.删除订单
	/api/order/delete_order
-	【权限】U
-	【说明】
- 	【参数】	

		{
		  "order_id": "14784316383"
		}
		
####6.确认订单
	/api/order/confirm_order
-	【权限】U
-	【说明】

	> 必须订单状态state=2，表示已发货
- 	【参数】	

		{
		  "order_id": "14784316383"
		}
		
####7.取消订单
	/api/order/cancel_order
-	【权限】U
-	【说明】

	> 必须订单状态state=0，表示下单未支付状态
- 	【参数】	

		{
		  "order_id": "14784316383",
		  "reason": ""
		}

####8.支付接口
	/api/order/pay
-	【权限】U
-	【说明】

	> 必须订单状态state=0，表示下单未支付状态
- 	【参数】	

		{
		"pay_params":
			{
			  "order_id": "14784316383",
			  "channel": "alipay_pc_direct",
			  "success_url": "www.sfm.com/order/pay_complete?order_id=400000002"
			}
		}
	
	> channel = "wx_pub_qr" or "alipay_pc_direct"   
	> success_url 支付宝方式下，支付成功的回调地址，一般用来展示支付结果页
		
####9.订单详情
	/api/order/get_order
-	【权限】U
-	【说明】
- 	【参数】

	{
		"order_id": "1111111"
	}
		
		

###额度卡接口列表

####1.额度卡信息
	/api/credit_card/detail
-	【权限】U
-	【说明】

	> 额度卡展示了订单的额度卡状态，必须订单状态state=1表示已付款
- 	【参数】

		{
		  "type": "all",
		  "page":1,
		  "count":10
		}
		
	>type= all,need_pay,over_time,has_pay

####2.额度卡付款
	/api/credit_card/pay
-	【权限】U
-	【说明】

	> 
- 	【参数】

		{
		"pay_params":
			{
			  "order_id": "14784316383",
			  "channel": "alipay_pc_direct",
			  "success_url": "www.sfm.com/order/pay_complete?order_id=400000002"
			}
		}
	
	> channel = "wx_pub_qr" or "alipay_pc_direct"   
	> success_url 支付宝方式下，支付成功的回调地址，一般用来展示支付结果页
	



###支付回调接口列表

####1.支付回调
	/api/webhooks/pingpp
-	【权限】T
-	【说明】

	> 必须订单状态state=0，表示下单未支付状态
- 	【参数】	
		
		
####2.支付demo
	/api/static/pay-pc.html
-	【权限】T
-	【说明】

	> 必须订单状态state=0，表示下单未支付状态
- 	【参数】


###后台接口列表
####1.[后台]订单列表
	/api/order/list
-	【权限】T
-	【说明】
- 	【参数】

		{
		"u_id": "1", 
		"u_mobile": "1", 
		"order_id": "1", 
		"ctime_st": 0, 
		"ctime_ed": 99999999999, 
		"order_type": "all", 
		"page": 1, 
		"count": 10
		}


	>order_type:
	
		all				全部订单
		need_pay   		代付款 0
		need_send	 	代发货 1	
		need_receive	待收货 2
		complete		已完成 3
		cancel			已取消 4
		overtime		已过期 5
	>u_id：   用户id    
	
	>u_mobile 用户电话号码  
	
	>order_id 订单号

####2.[后台]发货,需要输入物流信息id
	/api/order/send_out
-	【权限】U
-	【说明】

	> 必须订单状态state=1，表示已支付状态
	> logistics_id 为该物流号
- 	【参数】	

		{
		  "order_id": "14784316383",
		  "logistics_id": "adbc111111",
		  "logistics": "申通快递"
		}
		
####3.[后台]额度卡列表
	/api/credit_card/get_credit_cards
-	【权限】T
-	【说明】

	> 
- 	【参数】
	
		{"u_name": "",
		 "u_mobile": "",
		 "channel": "",
		 "update_time_st": 0,
		 "update_time_dt": 99999999999, 
		 "page": 1,
		 "count": 10
		}

####4.[后台]订单详情
	/api/order/detail
-	【权限】T
-	【说明】

	> 返回信息channel_id表示付款方式，0 微信，1支付宝
- 	【参数】

		{
		  "order_id":"14801432052"
		}
		
####5.[后台]订单添加管理员备注
	/api/order/add_admin_note
-	【权限】T
-	【说明】

	> 
- 	【参数】

		{
		  "order_id":"14801432052",
		  "admin_note": "测试"
		}
		
####6.[后台]设置额度卡
	/api/credit_card/set_credit_cards
-	【权限】T
-	【说明】

	> 
- 	【参数】

		{
		  "card_id":"110",
		  "inc_amount": 100
		}
		
####7.[后台]额度卡详情
	/api/credit_card/get_card_detail
-	【权限】T
-	【说明】

	> 
- 	【参数】

		{
		  "card_id": "216147913256010",
		  "page": 1,
		  "count": 10
		}
		
		
		
		
		
		
		
		
		
	
	
	
	
	
	