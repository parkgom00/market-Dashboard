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
  function bpText(v) {
    var n = Number(v) || 0;
    var cls = n > 0 ? "up" : n < 0 ? "down" : "flat";
    return '<span class="' + cls + '">' + (n > 0 ? "▲ +" : n < 0 ? "▼ " : "") + n.toFixed(1) + "bp</span>";
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
        "<span>" + (e.market ? '<span class="muted">' + esc(e.market) + " · </span>" : "") + (e.time ? '<span class="muted">' + esc(e.time) + " </span>" : "") + (e.major ? "<b>" + esc(e.title) + "</b>" : esc(e.title)) +
        ((e.result || []).length ? '<div class="evres">' + e.result.map(function (r) { return "<div>" + esc(r) + "</div>"; }).join("") + "</div>" : "") +
        "</span></div>";
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
    var br = u.brief || null;
    var h = sampleNote(u) + "<h2>미국장 마감 &amp; 국장 대응</h2>";
    h += '<div class="muted" style="margin:-6px 0 10px">' + esc(u.asOf || "") + "</div>";

    // 1) 지수·금리·환율·원자재
    var groups = [];
    (u.indices || []).forEach(function (i) {
      var g = groups.filter(function (x) { return x.name === (i.group || "지수"); })[0];
      if (!g) { g = { name: i.group || "지수", items: [] }; groups.push(g); }
      g.items.push(i);
    });
    groups.forEach(function (g) {
      h += '<div class="sub-title">' + esc(g.name) + '</div><div class="idx">' + g.items.map(function (i) {
        var chg = i.changeBp != null ? '<div class="pc">' + bpText(i.changeBp) + "</div>" : '<div class="pc">' + pctText(i.changePct) + "</div>";
        return '<div class="card"><div class="nm">' + esc(i.name) + "</div>" + chg + (i.close ? '<div class="nm">' + num(i.close) + (i.kind === "yield" ? "%" : "") + "</div>" : "") + "</div>";
      }).join("") + "</div>";
    });

    // 2) AI 브리핑
    if (br) {
      h += '<div class="card"><h3>간밤 미국장 이슈</h3><p class="para">' + esc(br.usMarket) + "</p>" +
        (br.sectorFlow ? '<div class="sub-title">업종 흐름</div><p class="para">' + esc(br.sectorFlow) + "</p>" : "") +
        (br.koreaImpact ? '<div class="sub-title">오늘 국장에 미칠 영향</div><p class="para">' + esc(br.koreaImpact) + "</p>" : "") +
        '<div class="muted">' + (br.grounded ? "AI가 구글 검색 근거로 정리한 내용입니다." : "검색 근거 없이 시세만 보고 해석한 내용입니다(원인은 확인되지 않았을 수 있음).") +
        " 참고용이며 투자 권유가 아닙니다.</div></div>";
      if ((br.news || []).length) {
        h += '<div class="card"><h3>주요 뉴스와 국내 파급</h3>' + br.news.map(function (n) {
          return '<div class="stock"><div class="nm">' + esc(n.title) + "</div><div>" + esc(n.fact) + "</div>" +
            (n.korea_impact ? '<div class="muted">국내 파급: ' + esc(n.korea_impact) + "</div>" : "") + "</div>";
        }).join("") + "</div>";
      }
      var chk = function (title, arr, cls) {
        if (!(arr || []).length) return "";
        return '<div class="card"><h3>' + title + "</h3>" + arr.map(function (c) {
          return '<div class="stock ' + cls + '"><div class="nm">' + esc(c.theme) + (c.us ? ' <span class="meta">' + esc(c.us) + "</span>" : "") + "</div>" +
            (c.cause ? "<div>" + esc(c.cause) + "</div>" : "") + (c.action ? '<div class="muted">점검 포인트: ' + esc(c.action) + "</div>" : "") + "</div>";
        }).join("") + "</div>";
      };
      h += chk("오늘 국장 체크 · 조심할 점", br.caution, "caution") + chk("오늘 국장 체크 · 눈여겨볼 곳", br.watch, "watch");
    } else if (u.briefStatus) {
      h += '<div class="card"><h3>간밤 미국장 이슈 · 국장 대응</h3><div class="muted">아직 AI 브리핑이 만들어지지 않았습니다. ' + esc(u.briefStatus) + "</div></div>";
    } else if ((u.summary || []).length) {
      h += '<div class="card"><h3>어제 미국장 이슈</h3><ul class="plain">' + u.summary.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul></div>";
    }

    // 3) 업종별 성과
    var sec = u.sectors || [];
    if (sec.length) {
      var sorted = sec.slice().sort(function (a, b) { return b.changePct - a.changePct; });
      var top = sorted.slice(0, 5), bot = sorted.slice(-5).reverse();
      var line = function (s) {
        return '<div class="stock row"><div><span class="nm">' + esc(s.name) + '</span> <span class="meta">' + esc(s.symbol) + (s.kr ? " · 국내: " + esc(s.kr) : "") + "</span></div>" + pctText(s.changePct) + "</div>";
      };
      h += '<div class="card"><h3>업종별 성과</h3><div class="sub-title">강한 업종 TOP 5</div>' + top.map(line).join("") +
        '<div class="sub-title">약한 업종 TOP 5</div>' + bot.map(line).join("") + "</div>";
      var gs = [];
      sec.forEach(function (s) {
        var g = gs.filter(function (x) { return x.name === s.group; })[0];
        if (!g) { g = { name: s.group, items: [] }; gs.push(g); }
        g.items.push(s);
      });
      h += '<div class="card"><h3>업종 전체 보기</h3>' + gs.map(function (g) {
        return "<details><summary>" + esc(g.name) + " (" + g.items.length + ")</summary>" +
          g.items.slice().sort(function (a, b) { return b.changePct - a.changePct; }).map(line).join("") + "</details>";
      }).join("") + '<div class="muted">업종은 대표 ETF 등락률 기준입니다.</div></div>';
    }

    // 4) 미국 특징주 ↔ 국내 연관주 (AI 연결)
    if (br && (br.connections || []).length) {
      h += "<h2>미국 특징주 ↔ 국내 연관주</h2>";
      br.connections.forEach(function (c) {
        h += '<div class="card"><div class="conn-sector"><b>' + esc(c.sector) + "</b>" +
          (c.sectorChange != null ? ' <span class="meta">업종</span> ' + pctText(c.sectorChange) : "") + "</div>" +
          '<div class="row"><div><span class="nm">' + esc(c.usName) + '</span> <span class="meta">' + esc(c.usTicker) + "</span></div>" +
          (c.usChange != null ? pctText(c.usChange) : '<span class="meta">' + (c.direction === "down" ? "약세" : "강세") + "</span>") + "</div>" +
          (c.cause ? '<div class="para">' + esc(c.cause) + "</div>" : "") +
          (c.logic ? '<div class="logic">연결 로직: ' + esc(c.logic) + "</div>" : "") +
          '<div class="sub-title">국내 연관주</div>' +
          (c.koreaPicks || []).map(function (p) {
            var nm = p.code ? '<a href="https://m.stock.naver.com/domestic/stock/' + encodeURIComponent(p.code) + '/total" target="_blank" rel="noopener noreferrer">' + esc(p.name) + "</a>" : esc(p.name);
            return '<div class="stock"><span class="nm">' + nm + '</span> <span class="str s' + p.strength + '">' + ["", "●○○", "●●○", "●●●"][p.strength] + "</span>" +
              (p.reason ? '<div class="meta">' + esc(p.reason) + "</div>" : "") + "</div>";
          }).join("") + "</div>";
      });
      h += '<div class="muted">●●● 직접 연관 · ●●○ 간접 · ●○○ 동조 가능성. AI가 검색으로 추정한 연결이라 실제 투자 전 확인이 필요합니다.</div>';
    }

    // 5) 고정 테마표 기반 (등락률은 실제 시세)
    if ((u.themes || []).length) {
      h += "<h2>테마별 미국 주도주</h2>";
      u.themes.forEach(function (t) {
        h += '<div class="card"><div class="row"><h3>' + esc(t.name) + "</h3>" + pctText(t.changePct) + "</div>";
        if (t.why) h += '<div class="muted">' + esc(t.why) + "</div>";
        h += (t.usStocks || []).map(function (s) {
          return '<div class="stock row"><div><span class="nm">' + esc(s.name) + '</span> <span class="meta">' + esc(s.ticker) + "</span></div>" + pctText(s.changePct) + "</div>";
        }).join("");
        if ((t.krStocks || []).length) {
          h += '<div class="sub-title">국내 연관주</div>' + t.krStocks.map(function (s) {
            return '<div class="stock"><span class="nm">' + esc(s.name) + '</span> <span class="meta">' + esc(s.code) + "</span>" +
              (s.link ? '<div class="meta">연결 로직: ' + esc(s.link) + "</div>" : "") + "</div>";
          }).join("");
        }
        h += "</div>";
      });
    }
    if (!(u.indices || []).length) h += '<div class="card empty">아직 수집된 데이터가 없습니다.</div>';
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

  var RANK_SHOW = 10;      // 처음에는 10위까지, '더보기'를 누르면 20위까지
  var liveMore = {};
  function rankBlock(key, items, extra) {
    if (!items || !items.length) return rankList(items);
    var open = !!liveMore[key + liveMarket];
    var shown = open ? items : items.slice(0, RANK_SHOW);
    var html = rankList(shown, extra);
    if (items.length > RANK_SHOW) {
      html += '<button type="button" class="morebtn" data-more="' + key + '">' + (open ? "접기 ▲" : (RANK_SHOW + 1) + "~" + items.length + "위 더보기 ▼") + "</button>";
    }
    return html;
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

    if (m.gainers) h += '<div class="card"><h3>등락률 상위</h3>' + rankBlock("gainers", m.gainers) + "</div>";
    if (m.value) {
      h += '<div class="card"><h3>거래대금 상위</h3>' + rankBlock("value", m.value, function (s) {
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
        return { t: t, st: st, avg: t.rate != null ? Number(t.rate) : avg };
      }).sort(function (a, b) { return b.avg - a.avg; }).forEach(function (o) {
        h += '<div style="margin-bottom:12px"><div class="theme-head"><b>' + esc(o.t.name) + "</b>" + (o.t.total ? '<span class="meta"> 상승 ' + o.t.rise + "/" + o.t.total + "</span>" : "") + pctText(o.avg) + "</div>" +
          o.st.map(function (s) {
            return '<span class="sc ' + strengthClass(s.changePct) + '"><b>' + esc(s.name) + "</b> " + (Number(s.changePct) > 0 ? "+" : "") + (Number(s.changePct) || 0).toFixed(1) + "%</span>";
          }).join("") + "</div>";
      });
      if (!m.themes.length) h += '<div class="muted">테마 데이터가 없습니다.</div>';
      h += "</div>";
    }
    if (!m.gainers && !m.value && !m.themes) h += '<div class="card empty">이 시장은 아직 표시할 데이터가 없습니다.</div>';
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
      var mb = ev.target.closest("[data-more]");
      if (mb) { var k = mb.getAttribute("data-more") + liveMarket; liveMore[k] = !liveMore[k]; renderLive(); return; }
      var b = ev.target.closest("[data-lm]");
      if (b) { liveMarket = b.getAttribute("data-lm"); renderLive(); }
    });
  }

  /* ---------- 3장: 유튜브 ---------- */
  function renderYouTube() {
    var root = $("#tab-youtube");
    var y = D.youtube || {};
    var hasAI = (y.channels || []).some(function (c) { return (c.videos || []).some(function (v) { return v.ai && v.ai.keySummary; }); });
    var h = sampleNote(y) + "<h2>유튜브 최신 영상</h2>" +
      '<div class="muted">' + (hasAI ? "AI(제미나이)가 영상을 보고 정리한 요약입니다. 참고용이니 중요한 내용은 원본 영상으로 확인하세요." : "채널별 최신 영상 목록입니다. ‘재미나이로 요약’을 누르면 요청문이 복사되고 재미나이가 열립니다. 입력창에 붙여넣기만 하세요.") + "</div>" +
      (y.asOf ? '<div class="muted">목록 기준 ' + esc(y.asOf) + "</div>" : "") +
      (hasAI && (y.aiStatus || []).length ? '<div class="muted">AI 요약 상태: ' + y.aiStatus.map(esc).join(" / ") + "</div>" : "");

    // 여러 채널이 같이 언급한 종목 (최근 요약 기준)
    var mention = {};
    (y.channels || []).forEach(function (c) {
      (c.videos || []).forEach(function (v) {
        if (!v.ai || !v.ai.sectors) return;
        v.ai.sectors.forEach(function (s) { (s.stocks || []).forEach(function (st) {
          mention[st.name] = mention[st.name] || {};
          mention[st.name][c.name] = true;
        }); });
      });
    });
    var multi = Object.keys(mention).filter(function (k) { return Object.keys(mention[k]).length >= 2; });
    if (multi.length) {
      h += '<div class="card"><h3>여러 채널이 함께 언급한 종목</h3>' + multi.map(function (k) {
        return '<div class="stock"><span class="nm">' + esc(k) + '</span> <span class="muted">' + esc(Object.keys(mention[k]).join(" · ")) + "</span></div>";
      }).join("") + "</div>";
    }

    (y.channels || []).forEach(function (c, ci) {
      var vs = c.videos || [];
      h += '<div class="card"><h3>' + esc(c.name) + "</h3>";
      if (!vs.length) h += '<div class="muted">아직 수집된 영상이 없습니다. 자동 갱신 후 표시됩니다.</div>';
      vs.forEach(function (v, vi) {
        var ai = v.ai && v.ai.keySummary ? v.ai : null;
        h += '<div class="stock"><div class="nm">' + esc(v.title) + "</div>" +
          '<div class="meta">' + esc(v.publishedAt) + ' · <a href="' + esc(safeUrl(v.url)) + '" target="_blank" rel="noopener noreferrer">영상 보기</a>' +
          (ai ? "" : ' · <a href="#" class="gem" data-c="' + ci + '" data-v="' + vi + '">재미나이로 요약</a>') + "</div>";
        if (ai) {
          h += '<div class="keysum">' + esc(ai.keySummary) + "</div>";
          var det = "";
          if ((ai.market || []).length) det += "<h4>시장·거시</h4><ul class='plain'>" + ai.market.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul>";
          (ai.sectors || []).forEach(function (s) {
            det += "<h4>" + esc(s.name) + "</h4>" + (s.point ? "<div>" + esc(s.point) + "</div>" : "") +
              (s.stocks || []).map(function (st) { return '<div class="muted">· <b>' + esc(st.name) + "</b> " + esc(st.note) + "</div>"; }).join("");
          });
          if ((ai.checkpoints || []).length) det += "<h4>체크포인트</h4><ul class='plain'>" + ai.checkpoints.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul>";
          if (det) h += "<details><summary>상세 리포트 펼치기</summary>" + det + "</details>";
        }
        h += "</div>";
      });
      if (c.handle) h += '<a class="btnlink" href="https://www.youtube.com/' + encodeURI(c.handle) + '/videos" target="_blank" rel="noopener noreferrer">채널 영상 전체 보기 ›</a>';
      h += "</div>";
    });
    root.innerHTML = h;
    root.onclick = function (ev) {
      var a = ev.target.closest("a.gem");
      if (!a) return;
      ev.preventDefault();
      var v = y.channels[+a.getAttribute("data-c")].videos[+a.getAttribute("data-v")];
      var text = "다음 유튜브 영상을 한국어로 요약해줘. 핵심 3~5줄, 언급된 종목·수치·전망 위주로.\n" + v.url;
      var done = function () { window.open("https://gemini.google.com/app", "_blank", "noopener"); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () { window.prompt("복사해서 재미나이에 붙여넣으세요", text); done(); });
      else { window.prompt("복사해서 재미나이에 붙여넣으세요", text); done(); }
    };
  }

  /* ---------- 공통: 종목 카드 (4장·5장) ---------- */
  var LETTER = ["a", "b", "c", "d", "e", "f", "g", "h"];
  function won억(v) {
    var n = Number(v) || 0;
    if (!n) return "-";
    return n >= 10000 ? (n / 10000).toFixed(n >= 100000 ? 0 : 1).replace(/\.0$/, "") + "조" : num(n) + "억";
  }
  function stockCard(s, tags, isKR, priceLabel) {
    var code = s.code || "";
    var link = isKR ? "https://m.stock.naver.com/domestic/stock/" + encodeURIComponent(code) + "/chart"
                    : "https://finance.yahoo.com/chart/" + encodeURIComponent(code);
    var h = '<div class="stock"><div class="row"><div><span class="nm">' + esc(s.name) + '</span> ' +
      '<a class="chartlink" href="' + link + '" target="_blank" rel="noopener noreferrer" title="차트 보기">📈</a> ' +
      '<span class="meta">' + esc(code) + "</span></div></div>";
    if ((tags || []).length) h += '<div class="tagrow">' + tags.map(function (t) {
      return '<span class="rt-line"><span class="rtag rt-' + t.k + '">' + esc(t.text) + "</span>" +
        (t.title ? '<span class="rlabel rl-' + t.k + '">' + esc(t.title) + "</span>" : "") + "</span>";
    }).join("") + "</div>";
    var chips = "";
    if (s.market) chips += '<span class="chip mk-' + esc(s.market.toLowerCase()) + '">' + esc(s.market) + "</span>";
    if (s.sector) chips += '<span class="chip">' + esc(s.sector) + "</span>";
    if (chips) h += "<div>" + chips + "</div>";
    h += '<div class="pricerow"><span class="lbl">' + (priceLabel || "현재가") + '</span> <b class="up">' + num(s.close) + "</b>" +
      (s.prevClose ? ' <span class="lbl">전일종가</span> <span class="blk">' + num(s.prevClose) + "</span>" : "") +
      (s.changePct != null ? " " + pctText(s.changePct) : "") + "</div>";
    var ex = [];
    if (s.marcap) ex.push("시총 " + won억(s.marcap));
    if (s.value) ex.push("거래대금 " + won억(s.value));
    if (ex.length) h += '<div class="meta">' + ex.join(" · ") + "</div>";
    return h;
  }

  /* ---------- 4장: 중장기 ---------- */
  function renderLong() {
    var root = $("#tab-long");
    var L = D.longterm || {};
    var market = "kr";
    var rules = L.rules || [];
    var ruleLabel = {};
    var ruleIds = rules.map(function (r) { return r.id; });
    rules.forEach(function (r) { ruleLabel[r.id] = r.label; });
    var maText = function (v) { return v ? num(v) : "-"; };

    function draw() {
      var h = "<h2>중장기 투자</h2>";
      h += '<div class="card"><h3>적용 규칙</h3><ul class="plain">' +
        rules.map(function (r, i) { return '<li><span class="rtag rt-' + i + '">' + LETTER[i] + "</span> <b>" + esc(r.label) + "</b> — " + esc(r.desc) + "</li>"; }).join("") + "</ul></div>";
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
          var tags = (s.matched || []).map(function (m) {
            var i = Math.max(0, ruleIds.indexOf(m));
            return { k: i, text: LETTER[i] || "?", title: ruleLabel[m] || m };
          });
          return stockCard(s, tags, market === "kr", "종가") +
            '<div class="meta">240일선 ' + maText(s.ma240) + " · 480일선 " + maText(s.ma480) + "</div>" +
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

  /* ---------- 5장: 단기 (유형 A 종가배팅주: 세부 A1·A2·A3, 각 5종목) ---------- */
  function renderShort() {
    var root = $("#tab-short");
    var S = D.shortterm || {};
    var types = S.types || [];
    var typeId = types.length ? types[0].id : "";
    var sub = "";

    function draw() {
      var t = types.filter(function (x) { return x.id === typeId; })[0];
      var h = sampleNote(S) + "<h2>단기 트레이딩</h2>";
      h += seg(types.map(function (x) { return { id: x.id, label: "유형 " + x.id + (x.name ? " " + x.name : "") }; }), typeId, "data-ty");
      if (!t) {
        h += '<div class="card empty">등록된 유형이 없습니다.</div>';
        root.innerHTML = h; return;
      }
      h += '<div class="card"><div class="row"><h3>' + esc(t.name) + '</h3><span class="chip">' + esc(t.timeframe) + "</span></div>" +
        (t.desc ? '<div class="muted">' + esc(t.desc) + "</div>" : "") +
        '<div class="muted">확인 시간대 ' + esc(S.window || "") + " · 갱신 " + esc(S.asOf || "-") + "</div>" +
        (S.status ? '<div class="muted">' + esc(S.status) + "</div>" : "") + "</div>";
      var subs = t.subtypes || [];
      if (subs.length) {
        if (!sub || !subs.some(function (x) { return x.id === sub; })) sub = subs[0].id;
        h += '<div class="seg">' + subs.map(function (x, i) {
          return '<button type="button" data-sb="' + esc(x.id) + '" class="' + (x.id === sub ? "on" : "") + '"><span class="rtag rt-' + i + '">' + esc(x.id) + "</span></button>";
        }).join("") + "</div>";
        var cur = subs.filter(function (x) { return x.id === sub; })[0];
        h += '<div class="card"><h3>' + esc(cur.name) + '</h3><div class="muted">' + esc(cur.desc || "") + "</div></div>";
        var items = cur.kr || [];
        if (!items.length) h += '<div class="card empty">지금 조건을 충족한 종목이 없습니다.</div>';
        else h += '<div class="card">' + items.map(function (s) { return stockRow(s, cur.id, subs.indexOf(cur), cur.short || cur.name); }).join("") + "</div>";
      } else {
        var its = t.kr || [];
        h += its.length ? '<div class="card">' + its.map(function (s) { return stockRow(s, "", 0); }).join("") + "</div>" : '<div class="card empty">조건을 충족한 종목이 없습니다.</div>';
      }
      root.innerHTML = h;
    }
    function stockRow(s, id, i, subName) {
      return stockCard(s, id ? [{ k: i, text: id, title: (subName || "") }] : [], true, "현재가") +
        (s.note ? '<div class="meta">' + esc(s.note) + "</div>" : "") + "</div>";
    }
    root.addEventListener("click", function (ev) {
      var a = ev.target.closest("[data-ty]");
      var b = ev.target.closest("[data-sb]");
      if (a) { typeId = a.getAttribute("data-ty"); sub = ""; draw(); }
      else if (b) { sub = b.getAttribute("data-sb"); draw(); }
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
