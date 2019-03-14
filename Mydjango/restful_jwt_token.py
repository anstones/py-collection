#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# jwt 过期/刷新策略

'''
* JWTToken刷新生命周期
* 1、登录成功后将用户的JWT生成的Token作为k、v存储到cache缓存里面(这时候k、v值一样)
* 2、当该用户在次请求时，通过JWTFilter层层校验之后会进入到doGetAuthenticationInfo进行身份验证

* 3、当该用户这次请求JWTToken值还在生命周期内，则会通过重新PUT的方式k、v都为Token值，缓存中的token值生命周期时间重新计算(这时候k、v值一样)

* 4、当该用户这次请求jwt生成的token值已经超时，但该token对应cache中的k还是存在，则表示该用户一直在操作只是JWT的token失效了，
    程序会给token对应的k映射的v值重新生成JWTToken并覆盖v值，该缓存生命周期重新计算
* 5、当该用户这次请求jwt在生成的token值已经超时，并在cache中不存在对应的k，则表示该用户账户空闲超时，返回用户信息已失效，请重新登录。

* 6、每次当返回为true情况下，都会给Response的Header中设置Authorization，该Authorization映射的v为cache对应的v值。
* 7、注：当前端接收到Response的Header中的Authorization值会存储起来，作为以后请求token使用
'''

# public boolean jwtTokenRefresh(String userName,String passWord){
#     HttpServletRequest httpServletRequest = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
#     HttpServletResponse response = ((ServletRequestAttributes)RequestContextHolder.getRequestAttributes()).getResponse();
#     String token = httpServletRequest.getHeader(Constants.TOKEN);
#     String cacheTokenKey = String.valueOf(EhcacheUtils.getInstance().get("matedataManagement", token));
#     System.out.println(cacheTokenKey == null);
#     if(!StringUtils.isEmpty(cacheTokenKey) && !cacheTokenKey.equals("null")){
#     if (!JWTUtil.verify(token, userName, passWord)) {
#         String newAuthorization=JWTUtil.sign(userName, passWord);
#         EhcacheUtils.getInstance().put("matedataManagement", cacheTokenKey, newAuthorization, JWTUtil.getExpireTime()/1000);
#     }else {
#         EhcacheUtils.getInstance().put("matedataManagement", cacheTokenKey, cacheTokenKey,JWTUtil.getExpireTime()/1000);
#     }
#     response.setHeader("Authorization", String.valueOf(EhcacheUtils.getInstance().get("matedataManagement", cacheTokenKey)));
#     return true;
#     } 
#     return false;
# }


from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import RefreshJSONWebToken
from rest_framework_jwt.views import verify_jwt_token



