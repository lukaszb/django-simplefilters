import{_ as s,c as n,o as a,a as t}from"./app.5c24c556.js";const w='{"title":"DRF","description":"","frontmatter":{},"headers":[{"level":2,"title":"Filterset","slug":"filterset"},{"level":2,"title":"Viewset","slug":"viewset"},{"level":2,"title":"View","slug":"view"}],"relativePath":"guide/drf.md"}',e={},p=t(`<h1 id="drf" tabindex="-1">DRF <a class="header-anchor" href="#drf" aria-hidden="true">#</a></h1><h2 id="filterset" tabindex="-1">Filterset <a class="header-anchor" href="#filterset" aria-hidden="true">#</a></h2><p>Now let&#39;s take a look at the <code>filtersets.py</code> - here we define filtering of our viewset.</p><div class="language-python"><pre><code><span class="token comment"># filtersets.py</span>
<span class="token keyword">import</span> simplefilters <span class="token keyword">as</span> filters


<span class="token keyword">class</span> <span class="token class-name">Todo</span><span class="token punctuation">(</span>filters<span class="token punctuation">.</span>FilterSet<span class="token punctuation">)</span><span class="token punctuation">:</span>

    <span class="token decorator annotation punctuation">@filters<span class="token punctuation">.</span>CharFilter</span><span class="token punctuation">(</span>many<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
    <span class="token keyword">def</span> <span class="token function">filter_status</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> qs<span class="token punctuation">,</span> values<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> qs<span class="token punctuation">.</span><span class="token builtin">filter</span><span class="token punctuation">(</span>status__in<span class="token operator">=</span>values<span class="token punctuation">)</span>

    <span class="token decorator annotation punctuation">@filters<span class="token punctuation">.</span>DateTimeFilter</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token keyword">def</span> <span class="token function">filter_modified_after</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> qs<span class="token punctuation">,</span> value<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> qs<span class="token punctuation">.</span><span class="token builtin">filter</span><span class="token punctuation">(</span>modified_at__gte<span class="token operator">=</span>value<span class="token punctuation">)</span>

</code></pre></div><h2 id="viewset" tabindex="-1">Viewset <a class="header-anchor" href="#viewset" aria-hidden="true">#</a></h2><p>Here is a pretty standard viewset for <code>Todo</code> model. Note that at this point we simply replace DRF&#39;s <code>filters</code> with <code>simplefilters</code>.</p><div class="language-python"><div class="highlight-lines"><br><br><br><br><br><div class="highlighted">\xA0</div><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br></div><pre><code><span class="token comment"># views.py</span>
<span class="token keyword">from</span> <span class="token punctuation">.</span> <span class="token keyword">import</span> filtersets
<span class="token keyword">from</span> <span class="token punctuation">.</span> <span class="token keyword">import</span> models
<span class="token keyword">from</span> <span class="token punctuation">.</span> <span class="token keyword">import</span> serializers
<span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>viewsets <span class="token keyword">import</span> ModelViewSet
<span class="token keyword">import</span> simplefilters <span class="token keyword">as</span> filters


<span class="token keyword">class</span> <span class="token class-name">TodoViewSet</span><span class="token punctuation">(</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span>
    queryset <span class="token operator">=</span> models<span class="token punctuation">.</span>Todo<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    serializer_class <span class="token operator">=</span> serializers<span class="token punctuation">.</span>Todo
    filter_backends <span class="token operator">=</span> <span class="token punctuation">[</span>filters<span class="token punctuation">.</span>DjangoFilterBackend<span class="token punctuation">]</span>
    filter_class <span class="token operator">=</span> filtersets<span class="token punctuation">.</span>Todo

    <span class="token keyword">class</span> <span class="token class-name">Meta</span><span class="token punctuation">:</span>
        model <span class="token operator">=</span> models<span class="token punctuation">.</span>Todo


todo_list <span class="token operator">=</span> TodoViewSet<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span><span class="token punctuation">{</span><span class="token string">&#39;get&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;list&#39;</span><span class="token punctuation">}</span><span class="token punctuation">)</span>

</code></pre></div><h2 id="view" tabindex="-1">View <a class="header-anchor" href="#view" aria-hidden="true">#</a></h2><p>It&#39;s easy to use filtersets at plain DRF api views too.</p><div class="language-python"><pre><code><span class="token keyword">from</span> <span class="token punctuation">.</span> <span class="token keyword">import</span> filtersets
<span class="token keyword">from</span> <span class="token punctuation">.</span> <span class="token keyword">import</span> models
<span class="token keyword">from</span> <span class="token punctuation">.</span> <span class="token keyword">import</span> serializers
<span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>decorators <span class="token keyword">import</span> api_view
<span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response
<span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>viewsets <span class="token keyword">import</span> ModelViewSet
<span class="token keyword">import</span> simplefilters <span class="token keyword">as</span> filters

<span class="token decorator annotation punctuation">@api_view</span><span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token string">&#39;GET&#39;</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
<span class="token keyword">def</span> <span class="token function">todo_list</span><span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    queryset <span class="token operator">=</span> models<span class="token punctuation">.</span>Todo<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    fs <span class="token operator">=</span> filtersets<span class="token punctuation">.</span>Todo<span class="token punctuation">(</span><span class="token punctuation">)</span>
    qs <span class="token operator">=</span> fs<span class="token punctuation">.</span>perform_filtering<span class="token punctuation">(</span>request<span class="token punctuation">,</span> queryset<span class="token punctuation">)</span>
    serializer <span class="token operator">=</span> serializers<span class="token punctuation">.</span>Todo<span class="token punctuation">(</span>qs<span class="token punctuation">,</span> many<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> Response<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>data<span class="token punctuation">)</span>
</code></pre></div>`,10),o=[p];function c(l,i,r,u,k,d){return a(),n("div",null,o)}var m=s(e,[["render",c]]);export{w as __pageData,m as default};
