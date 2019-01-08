# Spring Boot 기반 Spring Security 회원가입 / 로그인 구현하기

참조: https://xmfpes.github.io/spring/spring-security/

스프링 부트 환경에서 BCryptPasswordEncoder를 이용한 회원가입 암호화 / Spring Security를 이용한 로그인 구현

## 시큐리티의 구조

웹에서 스프링 시큐리티는 기본적으로 아래와 같이 필터 기반으로 동작한다.

많은 필터들이 존재하며, DispatcherServlet 을 호출하기 전에 거치게 된다.

setOrder로 필터간의 순서나 우선순위를 정해서 커스터마이징 할 수도 있다.

![security-filters](./images/security-filters.png)

## 프로젝트에 Spring Security 적용하기

Maven

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```


Gradle

```
compile("org.springframework.boot:spring-boot-starter-security")
```

위와 같이 디펜던시를 추가한 다음에 적절한 패키지를 생성하고, SecurityConfig 클래스를 추가한다. 패키지는 스프링 프로젝트의 패키지 하부에 있어야 한다.

```java
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

}
```

위와같이 설정해주면, 이제 사이트 전체가 잠겨서, 비밀번호를 쳐야 접근할 수 있게 된다. 원활한 프로젝트 진행을 위해 일단 페이지의 인증을 해제하자.

```java
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

	@Override
	public void configure(WebSecurity web) throws Exception
	{
		web.ignoring().antMatchers("/css/**", "/script/**", "image/**", "/fonts/**", "lib/**");
	}
	@Override
	protected void configure(HttpSecurity http) throws Exception
	{
		http.authorizeRequests()
			.antMatchers("/admin/**").hasRole("ADMIN")
			.antMatchers("/**").permitAll();
	}
}
```

위처럼 자원에 대한 접근을 풀고, 밑에서는 세부적인 설정을 따로 넣어준다. 일단은 원활한 진행을 위해 모든 경로에 대해 permitAll을 줬다.

## 적용된 Security 기반 회원가입 로직 추가하기

회원가입 이전에, 먼저 User정보를 구성할 테이블을 생성해야하는데 Security의 내부적으로 사용하는 클래스의 이름이 User이다. 겹치기 때문에 Account나 Member라는 이름을 사용해서 구현하자.

Member.java

```java
@Getter
@Setter
@Entity
@EqualsAndHashCode(of = "uid")
@ToString
public class Member {

	@Id
	@GeneratedValue
	private Long id;

	@Column(nullable = false, unique = true, length=50)
	private String uid;

	@Column(nullable = false, length=200)
	private String upw;

	@Column(nullable = false, unique = true, length=50)
	private String uemail;

	@CreationTimestamp
	private Date regdate;

	@UpdateTimestamp
	private Date updatedate;

	@OneToMany(cascade=CascadeType.ALL, fetch=FetchType.EAGER)
	@JoinColumn(name="uid")
	private List<MemberRole> roles;

}
```

`@OneToMany(cascade=CascadeType.ALL, fetch=FetchType.EAGER)` 설정은, cascade의 경우에는 엔티티들의 영속관계를 한번에 처리하지 못하기 때문에 이에 대한 cascade 설정을 추가하는것이고, member와 member_role을 둘다 동시에 조회하기 위해서 fetch 설정을 즉시 로딩으로 EAGER 설정을 주어야 에러가 발생하지 않습니다.

MemberRole.java

```java
@Getter
@Setter
@Entity
@EqualsAndHashCode(of = "rno")
@ToString
public class MemberRole {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long rno;

	private String roleName;
}
```

MemberRepository.java

```java
public interface MemberRepository extends CrudRepository<Member, Long> {

}
```

Member가 제대로 동작하는지 확인을 위한 테스트 코드 작성

```java
@RunWith(SpringRunner.class)
@SpringBootTest
@Log
public class MemberRepositoryTest {
	@Autowired
	MemberRepository memberRepository;

	@Test
	public void insertTest() {
		for(int i=0; i<100; i++) {
			Member member = new Member();
			member.setUid("user" + i);
			member.setUpw("pw" + i);
			member.setUemail("hihi@" + i);
			MemberRole role = new MemberRole();
			if(i <= 80) {
				role.setRoleName("BASIC");
			}else if(i <= 90) {
				role.setRoleName("MANAGER");
			}else {
				role.setRoleName("ADMIN");
			}
			member.setRoles(Arrays.asList(role));
			memberRepository.save(member);
		}
	}

	@Test
	public void testMember() {
		Optional<Member> result = Optional.ofNullable(memberRepository.findOne(85L));
		result.ifPresent(member -> log.info("member " + member));
	}
}
```


## 회원가입 로직 구현하기

위에서 제작한 Member와 MemberRole을 기반으로 회원가입 로직을 구현해보자.

MemberController.java

```java
@Controller
@RequestMapping("/member")
public class MemberController {

	@Autowired
	MemberRepository memberRepository;

	@PostMapping("")
	public String create(Member member) {
		MemberRole role = new MemberRole();
		BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
		member.setUpw(passwordEncoder.encode(member.getUpw()));
		role.setRoleName("BASIC");
		member.setRoles(Arrays.asList(role));
		memberRepository.save(member);
		return "redirect:/";
	}
}
```

스프링 시큐리티에서 지원해주는 BCryptPasswordEncoder를 이용해 회원 비밀번호를 암호화하고, MemberRole을 정의해 Member에 넣어주고 save를 했다.

signUp.html

```html
<form class="signup-form" action="/member" method="POST">
  <input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}" />
  <div class="row">
    <div class="input-field col s12">
      <input id="user_name" name="uid" type="text" class="validate"/>
      <label for="user_name">Username</label>
    </div>
  </div>
  <div class="row">
    <div class="input-field col s12">
      <input id="email" name="uemail" type="email" class="validate"/>
      <label for="email">Email</label>
    </div>
  </div>
  <div class="row">
    <div class="input-field col s12">
      <input id="password" name="upw" type="password" class="validate"/>
      <label for="password">Password</label>
    </div>
  </div>
  <input class="signup-btn waves-effect waves-light btn" type="submit" value="가입하기" />
</form>
```

각각 Member의 파라미터에 해당하는 값을 매칭하고, thymeleaf를 사용한 csrf 토큰 관련 설정을 추가해주면 된다. 이후 Get으로 signUp페이지에 연결하고 회원가입을 진행하면 정상적으로 회원가입이 될 거다.

![security-join](./images/security-join.png)

정상적으로 구현했다면, 위와같이 암호화된 비밀번호가 저장된것을 확인할 수 있다.

## 스프링 시큐리티 로그인 기능 구현하기

스프링 시큐리티에서 로그인 처리를 구현하려면 `SecurityConfig`에서 `AuthenticationManagerBuilder`를 주입해서 인증에 대한 처리를 해야 한다.

```java
@Autowired
public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {

}
```

위와같은 설정을 SecurityConfig에 넣고, 저기서 UserDetailsService를 이용해 로그인 인증 처리를 해주어야 한다.

이 과정에서 우리의 데이터베이스를 바탕으로 인증을 처리하기 위해서는 UserDetailsService를 구현하고 이를 HttpSecurity객체가 사용하도록 지정하면 우리가 만든 인증 로직을 바탕으로 동작하게 된다.

CustomUserDetailsService를 구현하면서 MemberRepository와 연동해 우리의 데이터베이스에 저장된 회원정보를 바탕으로 인증을 구현해야하는데 스프링 시큐리티의 User와 우리의 Member, GrantedAuthority와 우리의 MemberRole의 타입이 일치하지 않는 문제가 생긴다.

```java
public class CustomUserDetailsService implements UserDetailsService{

	@Autowired
	MemberRepository memberRepository;

	@Override
	public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
		return null;//반환할 타입이 Member와 맞지 않는다.
	}
}
```

위처럼 loadUserByUsername 메소드는 UserDetails를 반환하는데, MemberRepository에서 얻어온 Member와는 타입이 맞지 않는다. 이 타입을 맞춰주기 위해 Spring Security의 User를 상속하는 커스텀 유저 클래스를 추가해주자.

- SecurirtyMember 구현(SpringSecurity의 User 상속)

    ```java
    @Getter
    @Setter
    public class SecurityMember extends User {
    	private static final String ROLE_PREFIX = "ROLE_";
    	private static final long serialVersionUID = 1L;

    	public SecurityMember(Member member) {
    		super(member.getUid(), member.getUpw(), makeGrantedAuthority(member.getRoles()));
    	}

    	private static List<GrantedAuthority> makeGrantedAuthority(List<MemberRole> roles){
    		List<GrantedAuthority> list = new ArrayList<>();
    		roles.forEach(role -> list.add(new SimpleGrantedAuthority(ROLE_PREFIX + role.getRoleName())));
    		return list;
    	}
    }
    ```

    위에서 SecurityUser의 생성자로 Member를 받아서 Spring Security의 User타입과 우리가 구현한 Member의 값들을 매칭시켜 주자.

- CustomUserDetailsService 구현(UserDetailsService 구현)

    위에서 구현한 SecurityMember를 바탕으로 아까 타입이 맞지않아 구현하지 못한 CustomUserDetailsService를 구현하자.

    ```java
    @Service
    public class CustomUserDetailsService implements UserDetailsService{

    	@Autowired
    	MemberRepository memberRepository;

    	@Override
    	public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
    		return
    				Optional.ofNullable(memberRepository.findByUemail(email))
    				.filter(m -> m!= null)
    				.map(m -> new SecurityMember(m)).get();
    	}
    }
    ```

    `@Service` 어노테이션으로 빈으로 등록해주어야 정상적으로 작동하게 된다.

- Config 파일에 인증 관련 설정 추가하기

    ```java
    @Bean
    public PasswordEncoder passwordEncoder() {
      return new BCryptPasswordEncoder();
    }
    @Autowired
    public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
      auth.userDetailsService(customUserDetailsService).passwordEncoder(passwordEncoder());
    }
    ```

    auth에 userDetailsService에 우리가 만든 customUserDetailsService를 등록하고, passwordEncoder에 우리가 회원가입 로직을 만들때 사용한 Encoder를 등록해주자.

- Login Url 등록하기

    ```java
    @Override
    protected void configure(HttpSecurity http) throws Exception
    {
    	http.authorizeRequests()
    		.antMatchers("/admin/**").hasRole("ADMIN")
    		.antMatchers("/**").permitAll()
    		.and().formLogin()
    		.loginPage("/login")
    		.loginProcessingUrl("/login")
    		.defaultSuccessUrl("/")
        	.failureUrl("/login")
        	.and()
        	.logout();
    }
    ```

    `loginPage`는 로그인 뷰 페이지를 연결하고, `loginProcessingUrl`은 Post로 로그인을 처리할 Url

    `SucessUrl`은 로그인 성공 후 이동할 페이지, `failureUrl`은 실패 후 이동할 페이지를 지정한다.

    ```html
    <form class="login-form" method="POST">
      <input type ="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
      <div class="row">
        <div class="input-field col s12">
          <input id="email" type="email" name="username" class="validate"/>
          <label for="email">Email</label>
        </div>
      </div>
      <div class="row">
        <div class="input-field col s12">
          <input id="password" type="password" name="password" class="validate"/>
          <label for="password">Password</label>
        </div>
      </div>
      <input class="login-btn waves-effect waves-light btn" type="submit" value="로그인" />
    </form>
    ```

    이제 로그인 뷰 페이지에 **username**으로 **name**을 지정해주어야 정상적으로 받을 수 있다.

    그리고 **csrf** 관련 설정을 위해 **thymeleaf**를 이용해 **csrf**토큰을 추가해주어야 요청을 정상적으로 받을 수 있다.

## 로그인 성공시의 부가적인 작업 추가하기

로그인 성공 시, 리다이렉트되기 전의 페이지로 이동시켜준다거나 하는 부가작업을 추가하기 위해서는 **SecurityConfig**의 **successHandler**에 핸들러를 등록해주어야 한다, 등록할 핸들러의 타입은 `AuthenticationSuccessHandler` 타입이기 때문에 `AuthenticationSuccessHandler`를 구현하면서 로그인 성공시 사용되는 핸들러인 `SavedRequestAwareAuthenticationSuccessHandler`를 상속받아 구현하고 **SecurityConfig**에 등록시켜 주면 된다.

그 전에, prevPage를 세션에 등록해서, 이전 페이지 정보를 저장해두자.

- 로그인 페이지 컨트롤러에서 세션에 이전 페이지 정보 넣기

    Referer 요청 헤더는 현재 요청된 페이지의 이전 페이지의 주소 정보를 포함한다. [Referer 관련 mozilla문서](https://developer.mozilla.org/ko/docs/Web/HTTP/Headers/Referer)

    ```java
    @GetMapping("/login")
    public String loginForm(HttpServletRequest req) {
        String referer = req.getHeader("Referer");
        req.getSession().setAttribute("prevPage", referer);
        return "login";
    }
    ```

- 이전 페이지 정보를 받아 Redirect하는 `SavedRequestAwareAuthenticationSuccessHandler` 구현하기

    `AuthenticationSuccessHandler`인터페이스를 구현하는 `SimpleUrlAuthenticationSuccessHandler`를 상속하는 `SavedRequestAwareAuthenticationSuccessHandler`를 상속해서 구현하면 된다.

    ```java
    public class CustomLoginSuccessHandler extends SavedRequestAwareAuthenticationSuccessHandler {
    	public CustomLoginSuccessHandler(String defaultTargetUrl) {
            setDefaultTargetUrl(defaultTargetUrl);
        }
        @Override
        public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response,
        	Authentication authentication) throws ServletException, IOException {
            HttpSession session = request.getSession();
            if (session != null) {
                String redirectUrl = (String) session.getAttribute("prevPage");
                if (redirectUrl != null) {
                    session.removeAttribute("prevPage");
                    getRedirectStrategy().sendRedirect(request, response, redirectUrl);
                } else {
                    super.onAuthenticationSuccess(request, response, authentication);
                }
            } else {
                super.onAuthenticationSuccess(request, response, authentication);
            }
        }
    }
    ```

- SecurityConfig에 해당 핸들러 등록하기

    SecurityConfig.java에 successHandler를 등록하고, 빈 형태로 등록해두면 된다.

    ```java
    http.successHandler(successHandler())

    @Bean
    public AuthenticationSuccessHandler successHandler() {
      return new CustomLoginSuccessHandler("/");//default로 이동할 url
    }
    ```

    이후 로그인 시에만 해당 페이지로 접근 가능하도록 막아두려면 아래와 같은 설정을 추가하면 된다.

    ```java
    .antMatchers("/board/**").authenticated()
    ```

    이제 /board의 경로에는 로그인 시에만 접근이 가능하도록 막히게 된다.

    다른 페이지에서 board에 접근해보고, 로그인 시에 원하는 페이지로 정상적으로 이동되는지 테스트해보자.

## 전체 SecurityConfig 파일

```java
@EnableWebSecurity
@EnableOAuth2Client
public class SecurityConfig extends WebSecurityConfigurerAdapter {
	@Autowired
	CustomUserDetailsService customUserDetailsService;

	@Autowired
	OAuth2ClientContext oauth2ClientContext;

	@Override
	public void configure(WebSecurity web) throws Exception
	{
		web.ignoring().antMatchers("/css/**", "/script/**", "image/**", "/fonts/**", "lib/**");
	}
	@Override
	protected void configure(HttpSecurity http) throws Exception
	{
		http.authorizeRequests()
			.antMatchers("/admin/**").hasRole("ADMIN")
			.antMatchers("/board/**").authenticated()
			.antMatchers("/**").permitAll()
			.and().formLogin()
			.loginPage("/login")
			.loginProcessingUrl("/login")
			.defaultSuccessUrl("/")
			.successHandler(successHandler())
    			.failureUrl("/login")
    			.and()
    			.logout()
    			.and()
    			.addFilterBefore(ssoFilter(), BasicAuthenticationFilter.class);
	}

	@Bean
	public AuthenticationSuccessHandler successHandler() {
	    return new CustomLoginSuccessHandler("/defaultUrl");
	}

	@Bean
	public PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}

	@Autowired
	public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
		auth.userDetailsService(customUserDetailsService).passwordEncoder(passwordEncoder());
	}


	private Filter ssoFilter() {
	  CompositeFilter filter = new CompositeFilter();
	  List<Filter> filters = new ArrayList<>();
	  filters.add(ssoFilter(facebook(), "/login/facebook"));
	  filters.add(ssoFilter(github(), "/login/github"));
	  filter.setFilters(filters);
	  return filter;
	}

	private Filter ssoFilter(ClientResources client, String path) {
	  OAuth2ClientAuthenticationProcessingFilter filter = new OAuth2ClientAuthenticationProcessingFilter(path);
	  OAuth2RestTemplate template = new OAuth2RestTemplate(client.getClient(), oauth2ClientContext);
	  filter.setRestTemplate(template);
	  UserInfoTokenServices tokenServices = new UserInfoTokenServices(
	      client.getResource().getUserInfoUri(), client.getClient().getClientId());
	  tokenServices.setRestTemplate(template);
	  filter.setTokenServices(tokenServices);
	  return filter;
	}

	class ClientResources {
	  @NestedConfigurationProperty
	  private AuthorizationCodeResourceDetails client = new AuthorizationCodeResourceDetails();
	  @NestedConfigurationProperty
	  private ResourceServerProperties resource = new ResourceServerProperties();
	  public AuthorizationCodeResourceDetails getClient() {
	    return client;
	  }
	  public ResourceServerProperties getResource() {
	    return resource;
	  }
	}

	@Bean
	@ConfigurationProperties("github")
	public ClientResources github() {
	  return new ClientResources();
	}
	@Bean
	@ConfigurationProperties("facebook")
	public ClientResources facebook() {
	  return new ClientResources();
	}

	@Bean
	public FilterRegistrationBean oauth2ClientFilterRegistration(
	    OAuth2ClientContextFilter filter) {
	  FilterRegistrationBean registration = new FilterRegistrationBean();
	  registration.setFilter(filter);
	  registration.setOrder(-100);
	  return registration;
	}
}
```