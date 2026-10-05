(function () {
  "use strict";

  var D = window.DASH || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // 데이터 안의 글자가 화면 코드로 해석되지 않도록 안전 처리
  function esc(v) {
    return String(v == null ? "" : v).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function pad(n) { return n < 10 ? "0" + n : "" + n; }
  function ymd(y, m, d) { return y + "-" + pad(m + 1) + "-" + pad(d); }
  function pctText(v) {
    var n = Number(v) || 0;
    var cls = n > 0 ? "up" : n < 0 ? "down" : "flat";
    var sign = n > 0 ? "▲ +" : n < 0 ? "▼ " : "";
    return '<span class="' + cls + '">' + sign + n.toFixed(2) + "%</span>";
  }
  function num(v) { return Number(v || 0).toLocaleString("ko-KR"); }
  function sampleNote(o) {
    return o && o.sample ? '<div class="banner" style="margin:0 0 10px">이 탭은 아직 샘플 데이터입니다. 실제 시세·분석이 아닙니다.</div>' : "";
  }
  function safeUrl(u) { return /^https?:\/\//i.test(u || "") ? u : "#"; }

  /* ---------- 공통: 선택 버튼(세그먼트) ---------- */
  function seg(items, current, attr) {
    return '<div class="seg">' + items.map(function (it) {
      return '<button type="button" ' + attr + '="' + esc(it.id) + '" class="' + (it.id === current ? "on" : "") + '">' + esc(it.label) + "</button>";
    }).join("") + "</div>";
  }

  /* ---------- 1장: 캘린더 ---------- */
  var TYPE = {
    holiday: "휴장", econ: "경제지표", earnings: "실적", event: "이벤트"
  };

  function renderCalendar() {
    var root = $("#tab-calendar");
    var events = (D.calendar && D.calendar.events) || [];
    var now = new Date();
    var year = now.getFullYear(), month = now.getMonth();
    var selected = ymd(now.getFullYear(), now.getMonth(), now.getDate());
    var todayStr = selected;

    function eventsOn(date) { return events.filter(function (e) { return e.date === date; }); }

    function draw() {
      var first = new Date(year, month, 1).getDay();
      var days = new Date(year, month + 1, 0).getDate();
      var h = '<div class="cal-head"><button type="button" data-nav="-1" aria-label="이전 달">‹</button>' +
        "<strong>" + year + "년 " + (month + 1) + "월</strong>" +
        '<button type="button" data-nav="1" aria-label="다음 달">›</button></div>';

      h += '<div class="cal-grid">';
      ["일", "월", "화", "수", "목", "금", "토"].forEach(function (w, i) {
        h += '<div class="cal-dow ' + (i === 0 ? "sun" : i === 6 ? "sat" : "") + '">' + w + "</div>";
      });
      for (var b = 0; b < first; b++) h += '<div class="cal-day blank"></div>';
      for (var d = 1; d <= days; d++) {
        var ds = ymd(year, month, d);
        var dow = (first + d - 1) % 7;
        var evs = eventsOn(ds);
        var dots = evs.slice(0, 4).map(function (e) { return '<i class="dot ' + esc(e.type) + '"></i>'; }).join("");
        h += '<button type="button" data-date="' + ds + '" class="cal-day ' +
          (dow === 0 ? "sun " : dow === 6 ? "sat " : "") +
          (ds === todayStr ? "today " : "") + (ds === selected ? "sel" : "") + '">' +
          '<span class="n">' + d + '</span><span class="dots">' + dots + "</span></button>";
      }
      h += "</div>";

      h += '<div class="legend">' + Object.keys(TYPE).map(function (k) {
        return '<span><i class="dot ' + k + '"></i>' + TYPE[k] + "</span>";
      }).join("") + "</div>";

      var selEvs = eventsOn(selected);
      h += '<div class="card"><h3>' + esc(selected) + " 일정</h3>";
      h += selEvs.length ? selEvs.map(evRow).join("") : '<div class="muted">등록된 일정이 없습니다.</div>';
      h += "</div>";

      var prefix = year + "-" + pad(month + 1);
      var monthEvs = events.filter(function (e) { return e.date.indexOf(prefix) === 0; })
        .sort(function (a, b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : 0; });
      h += '<div class="card"><h3>이달의 주요 일정</h3>';
      h += monthEvs.length ? monthEvs.map(function (e) { return evRow(e, true); }).join("") : '<div class="muted">이 달에 등록된 일정이 없습니다.</div>';
      h += "</div>";

      root.innerHTML = '<h2>마켓 캘린더</h2>' + h;
    }

    function evRow(e, withDate) {
      return '<div class="ev">' +
        (withDate ? '<span class="d">' + esc(e.date.slice(5).replace("-", "/")) + "</span>" : "") +
        '<span class="tag ' + esc(e.type) + '">' + esc(TYPE[e.type] || e.type) + "</span>" +
        "<span>" + (e.market ? '<span class="muted">' + esc(e.market) + " · </span>" : "") + esc(e.title) + "</span></div>";
    }

    root.addEventListener("click", function (ev) {
      var nav = ev.target.closest("[data-nav]");
      var day = ev.target.closest("[data-date]");
      if (nav) {
        month += Number(nav.getAttribute("data-nav"));
        if (month < 0) { month = 11; year--; }
        if (month > 11) { month = 0; year++; }
        selected = ymd(year, month, 1);
        draw();
      } else if (day) {
        selected = day.getAttribute("data-date");
        draw();
      }
    });
    draw();
  }

  /* ---------- 2장: 미국장 ---------- */
  function renderUS() {
    var root = $("#tab-us");
    var u = D.usmarket || {};
    var h = sampleNote(u) + "<h2>전날 미국장 &amp; 특징주</h2>";
    h += '<div class="muted" style="margin:-6px 0 10px">' + esc(u.asOf || "") + "</div>";

    h += '<div class="idx">' + (u.indices || []).map(function (i) {
      return '<div class="card"><div class="nm">' + esc(i.name) + '</div><div class="pc">' + pctText(i.changePct) + "</div>" +
        (i.close ? '<div class="nm">' + num(i.close) + "</div>" : "") + "</div>";
    }).join("") + "</div>";

    if ((u.summary || []).length) {
      h += '<div class="card"><h3>어제 미국장 이슈</h3><ul class="plain">' +
        u.summary.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul></div>";
    }

    (u.themes || []).forEach(function (t) {
      h += '<div class="card"><div class="row"><h3>' + esc(t.name) + "</h3>" + pctText(t.changePct) + "</div>";
      if (t.why) h += '<div class="muted">' + esc(t.why) + "</div>";
      h += '<div class="sub-title">미국 특징주</div>';
      h += (t.usStocks || []).map(function (s) {
        return '<div class="stock row"><div><span class="nm">' + esc(s.name) + '</span> <span class="meta">' + esc(s.ticker) + "</span></div>" + pctText(s.changePct) + "</div>";
      }).join("");
      if ((t.krStocks || []).length) {
        h += '<div class="sub-title">국내 연관주</div>';
        h += t.krStocks.map(function (s) {
          return '<div class="stock"><div><span class="nm">' + esc(s.name) + '</span> <span class="meta">' + esc(s.code) + "</span></div>" +
            (s.link ? '<div class="meta">연결 로직: ' + esc(s.link) + "</div>" : "") + "</div>";
        }).join("");
      }
      h += "</div>";
    });
    if (!(u.themes || []).length && !(u.indices || []).length) h += '<div class="card empty">아직 수집된 데이터가 없습니다.</div>';
    root.innerHTML = h;
  }

  /* ---------- 특징주(실시간) ---------- */
  var LIVE_STRONG = 3;   // +3% 이상이면 '강한 종목'(빨강)
  var LIVE_WEAK = -3;    // -3% 이하이면 '약한 종목'(초록)
  var liveMarket = "kr";
  var liveStatus = "";   // 새로고침 결과 문구
  var liveBusy = false;

  function strengthClass(v) {
    var n = Number(v) || 0;
    return n >= LIVE_STRONG ? "strong" : n <= LIVE_WEAK ? "weak" : "";
  }
  function rankList(items, extra) {
    if (!items || !items.length) return '<div class="muted">데이터가 없습니다.</div>';
    return items.map(function (s, i) {
      return '<div class="rank"><div class="no">' + (i + 1) + '</div><div class="mid"><div class="nm">' + esc(s.name) + '</div>' +
        '<div class="meta">' + esc(s.code) + (s.price != null ? " · " + num(s.price) : "") + "</div></div>" +
        '<div class="rt">' + pctText(s.changePct) + (extra ? '<div class="meta">' + extra(s) + "</div>" : "") + "</div></div>";
    }).join("");
  }

  function renderLive() {
    var root = $("#tab-live");
    var L = D.live || {};
    var m = L[liveMarket] || {};
    var h = sampleNote(L) + '<div class="live-head"><h2>실시간 특징주</h2>' +
      '<button type="button" class="refresh' + (liveStatus.indexOf("실패") === 0 ? " err" : "") + '" id="live-refresh"' + (liveBusy ? " disabled" : "") + '>' +
      (liveBusy ? "불러오는 중…" : "↻ 새로고침") + "</button></div>";
    h += '<div class="muted" style="margin-bottom:8px">데이터 기준 ' + esc(L.asOf || "-") + (liveStatus ? " · " + esc(liveStatus) : "") + "</div>";
    h += seg([{ id: "kr", label: "국내" }, { id: "us", label: "미국" }], liveMarket, "data-lm");

    if (m.news) {
      h += '<div class="card"><h3>[특징주] 뉴스</h3>' +
        (m.news.length ? m.news.map(function (n) {
          return '<div class="news"><a href="' + esc(safeUrl(n.url)) + '" target="_blank" rel="noopener noreferrer">' + esc(n.title) + "</a>" +
            '<div class="meta">' + esc(n.time) + " · " + esc(n.source) + "</div></div>";
        }).join("") : '<div class="muted">뉴스가 없습니다.</div>') + "</div>";
    }
    if (m.gainers) h += '<div class="card"><h3>등락률 상위</h3>' + rankList(m.gainers) + "</div>";
    if (m.value) {
      h += '<div class="card"><h3>거래대금 상위</h3>' + rankList(m.value, function (s) {
        return s.valueEok != null ? num(s.valueEok) + "억" : "";
      }) + "</div>";
    }

    if (m.themes) {
      h += '<div class="card"><h3>테마별 강약</h3><div class="note">' +
        '<span class="lg"><i style="background:var(--strong)"></i>강함 ' + (LIVE_STRONG > 0 ? "+" : "") + LIVE_STRONG + "% 이상</span>" +
        '<span class="lg"><i style="background:var(--weak)"></i>약함 ' + LIVE_WEAK + "% 이하</span></div>";
      m.themes.map(function (t) {
        var st = (t.stocks || []).slice().sort(function (a, b) { return b.changePct - a.changePct; });
        var avg = st.length ? st.reduce(function (a, s) { return a + (Number(s.changePct) || 0); }, 0) / st.length : 0;
        return { t: t, st: st, avg: avg };
      }).sort(function (a, b) { return b.avg - a.avg; }).forEach(function (o) {
        h += '<div style="margin-bottom:12px"><div class="theme-head"><b>' + esc(o.t.name) + "</b>" + pctText(o.avg) + "</div>" +
          o.st.map(function (s) {
            return '<span class="sc ' + strengthClass(s.changePct) + '"><b>' + esc(s.name) + "</b> " + (Number(s.changePct) > 0 ? "+" : "") + (Number(s.changePct) || 0).toFixed(1) + "%</span>";
          }).join("") + "</div>";
      });
      if (!m.themes.length) h += '<div class="muted">테마 데이터가 없습니다.</div>';
      h += "</div>";
    }
    if (!m.news && !m.gainers && !m.value && !m.themes) h += '<div class="card empty">이 시장은 아직 표시할 데이터가 없습니다.</div>';
    h += '<div class="note">새로고침은 서버에 저장된 최신 데이터를 다시 불러옵니다. 데이터 자체는 수집 주기마다 갱신되므로 위의 "데이터 기준" 시각을 확인하세요.</div>';
    root.innerHTML = h;
  }

  function reloadLive() {
    if (liveBusy) return;
    liveBusy = true; liveStatus = ""; renderLive();
    var old = document.getElementById("live-js");
    var sc = document.createElement("script");
    sc.id = "live-js";
    sc.src = "data/live.js?t=" + Date.now();   // 주소 뒤에 시각을 붙여 항상 최신 파일을 받는다
    sc.onload = function () { liveBusy = false; liveStatus = "새로고침 " + new Date().toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit", second: "2-digit" }); renderLive(); };
    sc.onerror = function () { liveBusy = false; liveStatus = "실패: 데이터를 불러오지 못했습니다"; renderLive(); };
    if (old && old.parentNode) old.parentNode.removeChild(old);
    document.body.appendChild(sc);
  }

  function initLive() {
    renderLive();
    $("#tab-live").addEventListener("click", function (ev) {
      if (ev.target.closest("#live-refresh")) { reloadLive(); return; }
      var b = ev.target.closest("[data-lm]");
      if (b) { liveMarket = b.getAttribute("data-lm"); renderLive(); }
    });
  }

  /* ---------- 3장: 유튜브 ---------- */
  function renderYouTube() {
    var root = $("#tab-youtube");
    var y = D.youtube || {};
    var h = sampleNote(y) + "<h2>유튜브 최신 영상 요약</h2>";
    (y.channels || []).forEach(function (c) {
      h += '<div class="card"><h3>' + esc(c.name) + "</h3>";
      if (!(c.videos || []).length) h += '<div class="muted">아직 수집된 영상이 없습니다.</div>';
      (c.videos || []).forEach(function (v) {
        h += '<div class="stock"><div class="nm">' + esc(v.title) + "</div>" +
          '<div class="meta">' + esc(v.publishedAt) + ' · <a href="' + esc(safeUrl(v.url)) + '" target="_blank" rel="noopener noreferrer">원본 영상 보기</a></div>' +
          '<ul class="plain">' + (v.summary || []).map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul></div>";
      });
      h += "</div>";
    });
    if ((y.divergences || []).length) {
      h += '<div class="card"><h3>채널 간 의견이 엇갈리는 지점</h3><ul class="plain">' +
        y.divergences.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul></div>";
    }
    h += '<div class="muted">요약은 자동 생성된 참고용이며, 정확한 내용은 원본 영상을 확인하세요.</div>';
    root.innerHTML = h;
  }

  /* ---------- 4장: 중장기 ---------- */
  function renderLong() {
    var root = $("#tab-long");
    var L = D.longterm || {};
    var market = "kr";
    var rules = L.rules || [];
    var ruleLabel = {};
    rules.forEach(function (r) { ruleLabel[r.id] = r.label; });
    var maText = function (v) { return v ? num(v) : "-"; };

    function draw() {
      var h = "<h2>중장기 투자</h2>";
      h += '<div class="card"><h3>적용 규칙</h3><ul class="plain">' +
        rules.map(function (r) { return "<li><b>" + esc(r.label) + "</b> — " + esc(r.desc) + "</li>"; }).join("") + "</ul></div>";
      h += seg([{ id: "kr", label: "국내" }, { id: "us", label: "미국" }], market, "data-mk");
      var info = (L.scanInfo || {})[market];
      var items = L[market] || [];
      if (info && info.scanned) {
        h += '<div class="muted" style="margin:-4px 0 8px">기준일 ' + esc(info.asOf) + " · " + num(info.scanned) + "개 종목 스캔 · " + items.length + "개 충족</div>";
      }
      if (L.scanInfo && !(info && info.scanned)) {
        h += '<div class="card empty">아직 이 시장의 스캔 결과가 없습니다.</div>';
      } else if (!items.length) {
        h += '<div class="card empty">조건을 충족한 종목이 없습니다.</div>';
      } else {
        h += '<div class="card">' + items.map(function (s) {
          return '<div class="stock"><div class="row"><div><span class="nm">' + esc(s.name) + '</span> <span class="meta">' + esc(s.code) + "</span></div>" +
            '<span class="meta">종가 ' + num(s.close) + "</span></div>" +
            '<div class="meta">240일선 ' + maText(s.ma240) + " · 480일선 " + maText(s.ma480) + "</div>" +
            "<div>" + (s.matched || []).map(function (m) { return '<span class="chip">' + esc(ruleLabel[m] || m) + "</span>"; }).join("") + "</div>" +
            (s.note ? '<div class="meta">' + esc(s.note) + "</div>" : "") + "</div>";
        }).join("") + "</div>";
      }
      root.innerHTML = h;
    }
    root.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-mk]");
      if (b) { market = b.getAttribute("data-mk"); draw(); }
    });
    draw();
  }

  /* ---------- 5장: 단기 ---------- */
  function renderShort() {
    var root = $("#tab-short");
    var S = D.shortterm || {};
    var types = S.types || [];
    var typeId = types.length ? types[0].id : "";
    var market = "kr";

    function draw() {
      var t = types.filter(function (x) { return x.id === typeId; })[0];
      var h = sampleNote(S) + "<h2>단기 트레이딩</h2>";
      h += seg(types.map(function (x) { return { id: x.id, label: "유형 " + x.id }; }), typeId, "data-ty");
      h += seg([{ id: "kr", label: "국내" }, { id: "us", label: "미국" }], market, "data-mk");
      if (!t) {
        h += '<div class="card empty">등록된 유형이 없습니다.</div>';
      } else {
        h += '<div class="card"><div class="row"><h3>' + esc(t.name) + '</h3><span class="chip">' + esc(t.timeframe) + "</span></div>" +
          (t.desc ? '<div class="muted">' + esc(t.desc) + "</div>" : "") + "</div>";
        var items = t[market] || [];
        if (!items.length) {
          h += '<div class="card empty">조건을 충족한 종목이 없습니다.</div>';
        } else {
          h += '<div class="card">' + items.map(function (s) {
            return '<div class="stock"><div class="row"><div><span class="nm">' + esc(s.name) + '</span> <span class="meta">' + esc(s.code) + "</span></div>" +
              pctText(s.changePct) + "</div>" +
              '<div class="meta">종가 ' + num(s.close) + "</div>" +
              (s.note ? '<div class="meta">' + esc(s.note) + "</div>" : "") + "</div>";
          }).join("") + "</div>";
        }
      }
      root.innerHTML = h;
    }
    root.addEventListener("click", function (ev) {
      var a = ev.target.closest("[data-ty]");
      var b = ev.target.closest("[data-mk]");
      if (a) { typeId = a.getAttribute("data-ty"); draw(); }
      else if (b) { market = b.getAttribute("data-mk"); draw(); }
    });
    draw();
  }

  /* ---------- 탭 전환 (주소 뒤 #us 처럼 특정 탭으로 바로 열 수 있음) ---------- */
  var TABS = ["calendar", "us", "live", "youtube", "long", "short"];
  function show(name) {
    if (TABS.indexOf(name) < 0) name = "calendar";
    $$(".tab").forEach(function (t) { t.classList.toggle("active", t.id === "tab-" + name); });
    $$("#tabbar button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-tab") === name); });
    if (location.hash !== "#" + name) {
      try { history.replaceState(null, "", "#" + name); } catch (e) { location.hash = name; }
    }
    window.scrollTo(0, 0);
  }

  function init() {
    var meta = D.meta || {};
    if (meta.title) { $("#title").textContent = meta.title; document.title = meta.title; }
    $("#updated").textContent = meta.updatedAt ? "마지막 갱신 " + meta.updatedAt : "";
    $("#sample-banner").hidden = !meta.isSample;

    renderCalendar(); renderUS(); initLive(); renderYouTube(); renderLong(); renderShort();

    $("#tabbar").addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-tab]");
      if (b) show(b.getAttribute("data-tab"));
    });
    window.addEventListener("hashchange", function () { show(location.hash.replace("#", "")); });
    show(location.hash.replace("#", ""));
  }

  init();
})();
