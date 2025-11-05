# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# import os
# import csv
# import chardet
# from pathlib import Path
# from datetime import datetime

# class ForensicFileViewer:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("포렌식 파일 뷰어")
#         self.root.geometry("1400x900")
        
#         # 변수 초기화
#         self.selected_folder = None
#         self.categories = []
#         self.current_category = None
#         self.search_results = []
#         self.current_search_index = 0
#         self.file_tree_data = {}
#         self.current_file_path = None
#         self.current_file_content = None
#         self.view_mode = "table"  # table, text, hex
        
#         self.setup_ui()
        
#     def setup_ui(self):
#         # 메인 컨테이너
#         main_container = tk.Frame(self.root)
#         main_container.pack(fill=tk.BOTH, expand=True)
        
#         # ===== 상단: 헤더 =====
#         header_frame = tk.Frame(main_container, bg="#2c3e50", height=50)
#         header_frame.pack(fill=tk.X)
#         header_frame.pack_propagate(False)
        
#         title_label = tk.Label(header_frame, text="🔍 포렌식 파일 뷰어", 
#                               bg="#2c3e50", fg="white", font=("맑은 고딕", 14, "bold"))
#         title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
#         select_btn = tk.Button(header_frame, text="📁 폴더 선택", 
#                               command=self.select_folder,
#                               bg="#3498db", fg="white", font=("맑은 고딕", 10),
#                               relief=tk.FLAT, padx=15, pady=5, cursor="hand2")
#         select_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
#         # ===== 카테고리 바 (스크롤 가능) =====
#         category_frame = tk.Frame(main_container, bg="#ecf0f1", height=45)
#         category_frame.pack(fill=tk.X)
#         category_frame.pack_propagate(False)
        
#         # 카테고리 캔버스와 스크롤바
#         self.category_canvas = tk.Canvas(category_frame, bg="#ecf0f1", 
#                                         highlightthickness=0, height=45)
#         category_scrollbar = tk.Scrollbar(category_frame, orient=tk.HORIZONTAL, 
#                                          command=self.category_canvas.xview)
        
#         self.category_inner_frame = tk.Frame(self.category_canvas, bg="#ecf0f1")
#         self.category_canvas_window = self.category_canvas.create_window(
#             (0, 0), window=self.category_inner_frame, anchor="nw")
        
#         self.category_canvas.configure(xscrollcommand=category_scrollbar.set)
        
#         self.category_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#         category_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
#         # 스크롤 영역 업데이트
#         self.category_inner_frame.bind("<Configure>", 
#             lambda e: self.category_canvas.configure(scrollregion=self.category_canvas.bbox("all")))
        
#         # ===== 검색 바 =====
#         search_frame = tk.Frame(main_container, bg="#f8f9fa", height=45)
#         search_frame.pack(fill=tk.X)
#         search_frame.pack_propagate(False)
        
#         tk.Label(search_frame, text="검색:", bg="#f8f9fa", 
#                 font=("맑은 고딕", 9)).pack(side=tk.LEFT, padx=(20, 5), pady=10)
        
#         self.search_entry = tk.Entry(search_frame, font=("맑은 고딕", 10), width=40)
#         self.search_entry.pack(side=tk.LEFT, padx=5, pady=10)
#         self.search_entry.bind("<Return>", lambda e: self.search_files())
        
#         search_btn = tk.Button(search_frame, text="🔍 검색", command=self.search_files,
#                               bg="#28a745", fg="white", font=("맑은 고딕", 9),
#                               relief=tk.FLAT, padx=12, cursor="hand2")
#         search_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
#         prev_btn = tk.Button(search_frame, text="◀ 이전", command=self.prev_search_result,
#                             bg="#6c757d", fg="white", font=("맑은 고딕", 9),
#                             relief=tk.FLAT, padx=10, cursor="hand2")
#         prev_btn.pack(side=tk.LEFT, padx=2, pady=10)
        
#         next_btn = tk.Button(search_frame, text="다음 ▶", command=self.next_search_result,
#                             bg="#6c757d", fg="white", font=("맑은 고딕", 9),
#                             relief=tk.FLAT, padx=10, cursor="hand2")
#         next_btn.pack(side=tk.LEFT, padx=2, pady=10)
        
#         self.search_info_label = tk.Label(search_frame, text="", bg="#f8f9fa", 
#                                          font=("맑은 고딕", 9))
#         self.search_info_label.pack(side=tk.LEFT, padx=10)
        
#         # ===== PanedWindow로 크기 조절 가능한 레이아웃 =====
#         self.main_paned = tk.PanedWindow(main_container, orient=tk.VERTICAL, 
#                                          sashrelief=tk.RAISED, sashwidth=5)
#         self.main_paned.pack(fill=tk.BOTH, expand=True)
        
#         # 상단 패널 (좌측 트리 + 중앙 파일 목록)
#         top_panel = tk.Frame(self.main_paned)
#         self.main_paned.add(top_panel, minsize=300)
        
#         self.top_paned = tk.PanedWindow(top_panel, orient=tk.HORIZONTAL, 
#                                        sashrelief=tk.RAISED, sashwidth=5)
#         self.top_paned.pack(fill=tk.BOTH, expand=True)
        
#         # ===== 좌측: 파일 트리 =====
#         left_frame = tk.Frame(self.top_paned, bg="#f8f9fa")
#         self.top_paned.add(left_frame, minsize=200)
        
#         tree_label = tk.Label(left_frame, text="📁 폴더/파일 트리", 
#                              bg="#495057", fg="white", font=("맑은 고딕", 10, "bold"),
#                              anchor="w", padx=10, pady=8)
#         tree_label.pack(fill=tk.X)
        
#         tree_scroll_y = tk.Scrollbar(left_frame, orient=tk.VERTICAL)
#         tree_scroll_x = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL)
        
#         self.file_tree = ttk.Treeview(left_frame, 
#                                       yscrollcommand=tree_scroll_y.set,
#                                       xscrollcommand=tree_scroll_x.set)
#         tree_scroll_y.config(command=self.file_tree.yview)
#         tree_scroll_x.config(command=self.file_tree.xview)
        
#         tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
#         tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
#         self.file_tree.pack(fill=tk.BOTH, expand=True)
        
#         self.file_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
#         # ===== 중앙: 파일 목록 =====
#         center_frame = tk.Frame(self.top_paned)
#         self.top_paned.add(center_frame, minsize=300)
        
#         self.file_list_header = tk.Label(center_frame, text="📂 파일 목록", 
#                                          bg="#495057", fg="white", 
#                                          font=("맑은 고딕", 10, "bold"),
#                                          anchor="w", padx=10, pady=8)
#         self.file_list_header.pack(fill=tk.X)
        
#         file_list_scroll_y = tk.Scrollbar(center_frame, orient=tk.VERTICAL)
#         file_list_scroll_x = tk.Scrollbar(center_frame, orient=tk.HORIZONTAL)
        
#         self.file_listbox = tk.Listbox(center_frame, font=("맑은 고딕", 9),
#                                        yscrollcommand=file_list_scroll_y.set,
#                                        xscrollcommand=file_list_scroll_x.set)
#         file_list_scroll_y.config(command=self.file_listbox.yview)
#         file_list_scroll_x.config(command=self.file_listbox.xview)
        
#         file_list_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
#         file_list_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
#         self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
#         self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)
#         self.file_listbox.bind("<Button-3>", self.show_context_menu)
        
#         # ===== 하단: 파일 내용 표시 =====
#         bottom_frame = tk.Frame(self.main_paned)
#         self.main_paned.add(bottom_frame, minsize=200)
        
#         # 내용 헤더
#         content_header = tk.Frame(bottom_frame, bg="#6c757d", height=35)
#         content_header.pack(fill=tk.X)
#         content_header.pack_propagate(False)
        
#         self.content_title_label = tk.Label(content_header, text="📄 파일 내용", 
#                                            bg="#6c757d", fg="white", 
#                                            font=("맑은 고딕", 9, "bold"))
#         self.content_title_label.pack(side=tk.LEFT, padx=10, pady=8)
        
#         # 보기 모드 버튼
#         view_mode_frame = tk.Frame(content_header, bg="#6c757d")
#         view_mode_frame.pack(side=tk.RIGHT, padx=10)
        
#         self.table_btn = tk.Button(view_mode_frame, text="표", 
#                                    command=lambda: self.change_view_mode("table"),
#                                    bg="#495057", fg="white", font=("맑은 고딕", 8),
#                                    relief=tk.FLAT, padx=8, cursor="hand2")
#         self.table_btn.pack(side=tk.LEFT, padx=2)
        
#         self.text_btn = tk.Button(view_mode_frame, text="텍스트", 
#                                  command=lambda: self.change_view_mode("text"),
#                                  bg="#343a40", fg="white", font=("맑은 고딕", 8),
#                                  relief=tk.FLAT, padx=8, cursor="hand2")
#         self.text_btn.pack(side=tk.LEFT, padx=2)
        
#         self.hex_btn = tk.Button(view_mode_frame, text="HEX", 
#                                 command=lambda: self.change_view_mode("hex"),
#                                 bg="#343a40", fg="white", font=("맑은 고딕", 8),
#                                 relief=tk.FLAT, padx=8, cursor="hand2")
#         self.hex_btn.pack(side=tk.LEFT, padx=2)
        
#         # 내용 표시 영역
#         content_container = tk.Frame(bottom_frame)
#         content_container.pack(fill=tk.BOTH, expand=True)
        
#         # 테이블 뷰 (CSV용)
#         self.table_frame = tk.Frame(content_container)
        
#         table_scroll_y = tk.Scrollbar(self.table_frame, orient=tk.VERTICAL)
#         table_scroll_x = tk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL)
        
#         self.content_tree = ttk.Treeview(self.table_frame, 
#                                         yscrollcommand=table_scroll_y.set,
#                                         xscrollcommand=table_scroll_x.set)
#         table_scroll_y.config(command=self.content_tree.yview)
#         table_scroll_x.config(command=self.content_tree.xview)
        
#         table_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
#         table_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
#         self.content_tree.pack(fill=tk.BOTH, expand=True)
        
#         self.content_tree.bind("<Button-3>", self.show_content_context_menu)
#         self.content_tree.bind("<Button-1>", self.on_column_click)
        
#         # 텍스트 뷰 (TXT/HEX용)
#         self.text_frame = tk.Frame(content_container)
        
#         text_scroll_y = tk.Scrollbar(self.text_frame, orient=tk.VERTICAL)
#         text_scroll_x = tk.Scrollbar(self.text_frame, orient=tk.HORIZONTAL)
        
#         self.content_text = tk.Text(self.text_frame, wrap=tk.NONE,
#                                    font=("Consolas", 9),
#                                    yscrollcommand=text_scroll_y.set,
#                                    xscrollcommand=text_scroll_x.set)
#         text_scroll_y.config(command=self.content_text.yview)
#         text_scroll_x.config(command=self.content_text.xview)
        
#         text_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
#         text_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
#         self.content_text.pack(fill=tk.BOTH, expand=True)
        
#         self.content_text.bind("<Button-3>", self.show_content_context_menu)
        
#         # 하이라이트 태그 설정
#         self.content_text.tag_configure("highlight", background="yellow", foreground="black")
        
#         # 초기 뷰 설정
#         self.table_frame.pack(fill=tk.BOTH, expand=True)
        
#     def select_folder(self):
#         folder = filedialog.askdirectory(title="폴더 선택")
#         if folder:
#             self.selected_folder = folder
#             self.load_categories()
            
#     def load_categories(self):
#         """선택된 폴더의 최상위 하위 폴더들을 카테고리로 로드"""
#         if not self.selected_folder:
#             return
            
#         # 기존 카테고리 제거
#         for widget in self.category_inner_frame.winfo_children():
#             widget.destroy()
            
#         self.categories = []
        
#         try:
#             items = os.listdir(self.selected_folder)
#             for item in items:
#                 item_path = os.path.join(self.selected_folder, item)
#                 if os.path.isdir(item_path):
#                     self.categories.append(item)
                    
#             # 카테고리 버튼 생성
#             for idx, category in enumerate(self.categories):
#                 btn = tk.Button(self.category_inner_frame, text=f"📂 {category}",
#                               command=lambda c=category: self.select_category(c),
#                               bg="white", font=("맑은 고딕", 9),
#                               relief=tk.RAISED, padx=15, pady=8, cursor="hand2")
#                 btn.pack(side=tk.LEFT, padx=3, pady=5)
                
#             if self.categories:
#                 self.select_category(self.categories[0])
                
#         except Exception as e:
#             messagebox.showerror("오류", f"폴더 로드 실패: {str(e)}")
            
#     def select_category(self, category):
#         """카테고리 선택 시 좌측 트리에 해당 폴더 구조 표시"""
#         self.current_category = category
        
#         # 카테고리 버튼 활성화 표시
#         for widget in self.category_inner_frame.winfo_children():
#             if isinstance(widget, tk.Button):
#                 if category in widget["text"]:
#                     widget.config(bg="#2980b9", fg="white")
#                 else:
#                     widget.config(bg="white", fg="black")
                    
#         # 트리 초기화 및 로드
#         self.file_tree.delete(*self.file_tree.get_children())
#         category_path = os.path.join(self.selected_folder, category)
        
#         self.populate_tree("", category_path)
        
#     def populate_tree(self, parent, path):
#         """재귀적으로 트리 구조 생성"""
#         try:
#             items = os.listdir(path)
#             items.sort()
            
#             for item in items:
#                 item_path = os.path.join(path, item)
#                 is_dir = os.path.isdir(item_path)
                
#                 icon = "📁" if is_dir else "📄"
#                 node = self.file_tree.insert(parent, "end", text=f"{icon} {item}", 
#                                              values=(item_path,))
                
#                 if is_dir:
#                     # 하위 항목이 있으면 재귀 호출
#                     try:
#                         if os.listdir(item_path):
#                             self.populate_tree(node, item_path)
#                     except:
#                         pass
                        
#         except Exception as e:
#             print(f"트리 로드 오류: {str(e)}")
            
#     def on_tree_select(self, event):
#         """트리에서 항목 선택 시"""
#         selection = self.file_tree.selection()
#         if not selection:
#             return
            
#         item = selection[0]
#         values = self.file_tree.item(item, "values")
        
#         if values:
#             path = values[0]
#             if os.path.isdir(path):
#                 self.load_file_list(path)
#             else:
#                 self.display_file(path)
                
#     def load_file_list(self, folder_path):
#         """중앙 영역에 선택된 폴더의 파일 목록 표시"""
#         self.file_listbox.delete(0, tk.END)
        
#         folder_name = os.path.basename(folder_path)
        
#         try:
#             items = os.listdir(folder_path)
#             files = [f for f in items if os.path.isfile(os.path.join(folder_path, f))]
#             files.sort()
            
#             self.file_list_header.config(text=f"📂 {folder_name} ({len(files)}개 파일)")
            
#             for file in files:
#                 file_path = os.path.join(folder_path, file)
#                 size = os.path.getsize(file_path)
#                 size_str = self.format_size(size)
                
#                 self.file_listbox.insert(tk.END, f"📄 {file}  ({size_str})")
                
#         except Exception as e:
#             messagebox.showerror("오류", f"파일 목록 로드 실패: {str(e)}")
            
#     def format_size(self, size):
#         """파일 크기 포맷"""
#         for unit in ['B', 'KB', 'MB', 'GB']:
#             if size < 1024.0:
#                 return f"{size:.1f} {unit}"
#             size /= 1024.0
#         return f"{size:.1f} TB"
        
#     def on_file_select(self, event):
#         """파일 목록에서 파일 선택 시"""
#         selection = self.file_listbox.curselection()
#         if not selection:
#             return
            
#         idx = selection[0]
#         file_text = self.file_listbox.get(idx)
        
#         # 파일명 추출
#         file_name = file_text.split("📄 ")[1].split("  (")[0]
        
#         # 현재 선택된 트리 항목에서 경로 가져오기
#         tree_selection = self.file_tree.selection()
#         if tree_selection:
#             values = self.file_tree.item(tree_selection[0], "values")
#             if values:
#                 parent_path = values[0]
#                 if os.path.isdir(parent_path):
#                     file_path = os.path.join(parent_path, file_name)
#                 else:
#                     file_path = os.path.join(os.path.dirname(parent_path), file_name)
                    
#                 self.display_file(file_path)
                
#     def display_file(self, file_path):
#         """하단 영역에 파일 내용 표시"""
#         self.current_file_path = file_path
#         file_name = os.path.basename(file_path)
#         self.content_title_label.config(text=f"📄 {file_name}")
        
#         try:
#             file_ext = os.path.splitext(file_path)[1].lower()
            
#             if file_ext == '.csv':
#                 self.view_mode = "table"
#                 self.display_csv(file_path)
#             else:
#                 self.view_mode = "text"
#                 self.display_text(file_path)
                
#             self.update_view_buttons()
            
#         except Exception as e:
#             messagebox.showerror("오류", f"파일 표시 실패: {str(e)}")
            
#     def display_csv(self, file_path):
#         """CSV 파일을 테이블로 표시"""
#         # 테이블 프레임 표시
#         self.text_frame.pack_forget()
#         self.table_frame.pack(fill=tk.BOTH, expand=True)
        
#         # 기존 내용 제거
#         self.content_tree.delete(*self.content_tree.get_children())
        
#         # 인코딩 감지
#         encoding = self.detect_encoding(file_path)
        
#         try:
#             with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
#                 reader = csv.reader(f)
#                 rows = list(reader)
                
#             if not rows:
#                 return
                
#             # 헤더 설정
#             headers = [h.strip() for h in rows[0]]
#             self.content_tree["columns"] = headers
#             self.content_tree["show"] = "tree headings"
            
#             # 컬럼 설정
#             self.content_tree.column("#0", width=50, stretch=False)
#             self.content_tree.heading("#0", text="No")
            
#             for col in headers:
#                 self.content_tree.column(col, width=150, anchor="w")
#                 self.content_tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
                
#             # 데이터 삽입
#             for idx, row in enumerate(rows[1:], 1):
#                 # 컬럼 수에 맞게 데이터 조정
#                 row_data = row + [""] * (len(headers) - len(row))
#                 row_data = row_data[:len(headers)]
#                 self.content_tree.insert("", "end", text=str(idx), values=row_data)
                
#             self.current_file_content = rows
            
#         except Exception as e:
#             messagebox.showerror("오류", f"CSV 로드 실패: {str(e)}")
            
#     def display_text(self, file_path):
#         """텍스트 파일 표시"""
#         # 텍스트 프레임 표시
#         self.table_frame.pack_forget()
#         self.text_frame.pack(fill=tk.BOTH, expand=True)
        
#         # 기존 내용 제거
#         self.content_text.delete(1.0, tk.END)
        
#         # 인코딩 감지
#         encoding = self.detect_encoding(file_path)
        
#         try:
#             # 큰 파일 처리 (10MB 이상은 앞부분만)
#             file_size = os.path.getsize(file_path)
#             max_size = 10 * 1024 * 1024  # 10MB
            
#             if file_size > max_size:
#                 with open(file_path, 'rb') as f:
#                     content = f.read(max_size)
                    
#                 try:
#                     text = content.decode(encoding, errors='ignore')
#                     text += f"\n\n[파일이 너무 큽니다. 처음 10MB만 표시됩니다.]"
#                 except:
#                     text = self.to_hex(content)
#                     text += f"\n\n[파일이 너무 큽니다. 처음 10MB만 표시됩니다.]"
#             else:
#                 with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
#                     text = f.read()
                    
#             self.content_text.insert(1.0, text)
#             self.current_file_content = text
            
#         except Exception as e:
#             # 바이너리 파일인 경우 HEX로 표시
#             try:
#                 with open(file_path, 'rb') as f:
#                     content = f.read(max_size if file_size > max_size else file_size)
                    
#                 hex_text = self.to_hex(content)
#                 if file_size > max_size:
#                     hex_text += f"\n\n[파일이 너무 큽니다. 처음 10MB만 표시됩니다.]"
                    
#                 self.content_text.insert(1.0, hex_text)
#                 self.current_file_content = hex_text
#                 self.view_mode = "hex"
#                 self.update_view_buttons()
                
#             except Exception as e2:
#                 messagebox.showerror("오류", f"파일 표시 실패: {str(e2)}")
                
#     def to_hex(self, data):
#         """바이트 데이터를 HEX 문자열로 변환"""
#         hex_lines = []
#         for i in range(0, len(data), 16):
#             chunk = data[i:i+16]
#             hex_part = ' '.join(f'{b:02X}' for b in chunk)
#             ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
#             hex_lines.append(f"{i:08X}  {hex_part:<48}  {ascii_part}")
#         return '\n'.join(hex_lines)
        
#     def detect_encoding(self, file_path):
#         """파일 인코딩 감지"""
#         try:
#             with open(file_path, 'rb') as f:
#                 raw_data = f.read(10000)
#                 result = chardet.detect(raw_data)
#                 return result['encoding'] or 'utf-8'
#         except:
#             return 'utf-8'
            
#     def change_view_mode(self, mode):
#         """뷰 모드 변경"""
#         if not self.current_file_path:
#             return
            
#         self.view_mode = mode
        
#         if mode == "table":
#             if self.current_file_path.endswith('.csv'):
#                 self.display_csv(self.current_file_path)
#             else:
#                 messagebox.showinfo("알림", "CSV 파일만 표 형식으로 볼 수 있습니다.")
#                 return
#         elif mode == "text":
#             self.display_text(self.current_file_path)
#         elif mode == "hex":
#             self.display_hex_view()
            
#         self.update_view_buttons()
        
#     def display_hex_view(self):
#         """HEX 뷰 표시"""
#         self.table_frame.pack_forget()
#         self.text_frame.pack(fill=tk.BOTH, expand=True)
        
#         self.content_text.delete(1.0, tk.END)
        
#         try:
#             max_size = 10 * 1024 * 1024
#             file_size = os.path.getsize(self.current_file_path)
            
#             with open(self.current_file_path, 'rb') as f:
#                 content = f.read(max_size if file_size > max_size else file_size)
                
#             hex_text = self.to_hex(content)
#             if file_size > max_size:
#                 hex_text += f"\n\n[파일이 너무 큽니다. 처음 10MB만 표시됩니다.]"
                
#             self.content_text.insert(1.0, hex_text)
            
#         except Exception as e:
#             messagebox.showerror("오류", f"HEX 뷰 표시 실패: {str(e)}")
            
#     def update_view_buttons(self):
#         """뷰 모드 버튼 업데이트"""
#         self.table_btn.config(bg="#343a40" if self.view_mode != "table" else "#495057")
#         self.text_btn.config(bg="#343a40" if self.view_mode != "text" else "#495057")
#         self.hex_btn.config(bg="#343a40" if self.view_mode != "hex" else "#495057")
        
#     def sort_column(self, col):
#         """CSV 컬럼 정렬 (날짜만 정렬)"""
#         if not self.current_file_content:
#             return
            
#         # 현재 데이터 가져오기
#         data = []
#         for item in self.content_tree.get_children():
#             values = self.content_tree.item(item)['values']
#             data.append((item, values))
            
#         # 컬럼 인덱스 찾기
#         columns = self.content_tree["columns"]
#         if col not in columns:
#             return
#         col_idx = columns.index(col)
        
#         # 날짜 형식 감지 및 정렬
#         try:
#             # 첫 번째 값으로 날짜인지 확인
#             sample_value = data[0][1][col_idx] if data else ""
            
#             # 날짜 형식인지 확인
#             is_date = False
#             date_formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y', 
#                            '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S']
            
#             for fmt in date_formats:
#                 try:
#                     datetime.strptime(sample_value, fmt)
#                     is_date = True
#                     break
#                 except:
#                     continue
                    
#             if is_date:
#                 # 날짜 정렬
#                 reverse = getattr(self, f'sort_{col}_reverse', False)
                
#                 def parse_date(val):
#                     for fmt in date_formats:
#                         try:
#                             return datetime.strptime(val, fmt)
#                         except:
#                             continue
#                     return datetime.min
                    
#                 data.sort(key=lambda x: parse_date(x[1][col_idx]), reverse=reverse)
                
#                 # 정렬 방향 토글
#                 setattr(self, f'sort_{col}_reverse', not reverse)
                
#                 # 트리 업데이트
#                 for idx, (item, values) in enumerate(data):
#                     self.content_tree.move(item, '', idx)
                    
#                 # 헤더 표시 업데이트
#                 for column in columns:
#                     if column == col:
#                         arrow = "▼" if reverse else "▲"
#                         self.content_tree.heading(column, text=f"{column} {arrow}")
#                     else:
#                         self.content_tree.heading(column, text=column)
#             else:
#                 messagebox.showinfo("알림", "날짜 형식의 컬럼만 정렬 가능합니다.")
                
#         except Exception as e:
#             messagebox.showerror("오류", f"정렬 실패: {str(e)}")
            
#     def on_column_click(self, event):
#         """컬럼 헤더 클릭 이벤트"""
#         region = self.content_tree.identify_region(event.x, event.y)
#         if region == "heading":
#             column = self.content_tree.identify_column(event.x)
#             if column != '#0':
#                 col_idx = int(column.replace('#', '')) - 1
#                 columns = self.content_tree["columns"]
#                 if 0 <= col_idx < len(columns):
#                     self.sort_column(columns[col_idx])
                    
#     def search_files(self):
#         """파일 내용 검색"""
#         search_text = self.search_entry.get().strip()
#         if not search_text:
#             messagebox.showwarning("경고", "검색어를 입력하세요.")
#             return
            
#         if not self.selected_folder:
#             messagebox.showwarning("경고", "먼저 폴더를 선택하세요.")
#             return
            
#         self.search_results = []
#         self.current_search_index = 0
        
#         # 진행 표시
#         self.search_info_label.config(text="검색 중...")
#         self.root.update()
        
#         # 모든 파일 검색
#         for root_dir, dirs, files in os.walk(self.selected_folder):
#             for file in files:
#                 file_path = os.path.join(root_dir, file)
                
#                 try:
#                     # 파일 크기 확인 (너무 큰 파일은 스킵)
#                     if os.path.getsize(file_path) > 50 * 1024 * 1024:  # 50MB
#                         continue
                        
#                     encoding = self.detect_encoding(file_path)
                    
#                     with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
#                         content = f.read()
                        
#                     if search_text.lower() in content.lower():
#                         self.search_results.append({
#                             'path': file_path,
#                             'content': content
#                         })
                        
#                 except:
#                     continue
                    
#         # 검색 결과 표시
#         if self.search_results:
#             self.search_info_label.config(
#                 text=f"검색 결과: {len(self.search_results)}개 파일 (1/{len(self.search_results)})")
            
#             # 검색 결과 카테고리 추가
#             self.add_search_category()
            
#             # 첫 번째 결과 표시
#             self.show_search_result(0)
#         else:
#             self.search_info_label.config(text="검색 결과 없음")
#             messagebox.showinfo("검색 완료", "검색 결과가 없습니다.")
            
#     def add_search_category(self):
#         """검색 결과 카테고리 추가"""
#         # 기존 검색 카테고리 제거
#         for widget in self.category_inner_frame.winfo_children():
#             if isinstance(widget, tk.Button) and "🔍 검색 결과" in widget["text"]:
#                 widget.destroy()
                
#         # 새 검색 카테고리 추가
#         search_btn = tk.Button(self.category_inner_frame, text="🔍 검색 결과",
#                               command=self.show_search_results_tree,
#                               bg="#f39c12", fg="white", font=("맑은 고딕", 9),
#                               relief=tk.RAISED, padx=15, pady=8, cursor="hand2")
#         search_btn.pack(side=tk.LEFT, padx=3, pady=5)
        
#     def show_search_results_tree(self):
#         """검색 결과를 트리에 표시"""
#         self.file_tree.delete(*self.file_tree.get_children())
        
#         for idx, result in enumerate(self.search_results, 1):
#             file_name = os.path.basename(result['path'])
#             self.file_tree.insert("", "end", text=f"📄 {file_name}", 
#                                  values=(result['path'],))
                                 
#         # 카테고리 버튼 활성화 표시
#         for widget in self.category_inner_frame.winfo_children():
#             if isinstance(widget, tk.Button):
#                 if "🔍 검색 결과" in widget["text"]:
#                     widget.config(bg="#f39c12", fg="white")
#                 else:
#                     widget.config(bg="white", fg="black")
                    
#     def show_search_result(self, index):
#         """특정 검색 결과 표시 및 하이라이트"""
#         if not self.search_results or index < 0 or index >= len(self.search_results):
#             return
            
#         result = self.search_results[index]
#         self.display_file(result['path'])
        
#         # 검색어 하이라이트
#         search_text = self.search_entry.get().strip()
#         self.highlight_search_text(search_text)
        
#     def highlight_search_text(self, search_text):
#         """텍스트에서 검색어 하이라이트"""
#         if not search_text:
#             return
            
#         if self.view_mode in ["text", "hex"]:
#             # 기존 하이라이트 제거
#             self.content_text.tag_remove("highlight", "1.0", tk.END)
            
#             # 검색어 찾아서 하이라이트
#             start_pos = "1.0"
#             while True:
#                 pos = self.content_text.search(search_text, start_pos, 
#                                               stopindex=tk.END, nocase=True)
#                 if not pos:
#                     break
                    
#                 end_pos = f"{pos}+{len(search_text)}c"
#                 self.content_text.tag_add("highlight", pos, end_pos)
#                 start_pos = end_pos
                
#             # 첫 번째 결과로 스크롤
#             first_pos = self.content_text.search(search_text, "1.0", 
#                                                 stopindex=tk.END, nocase=True)
#             if first_pos:
#                 self.content_text.see(first_pos)
                
#     def prev_search_result(self):
#         """이전 검색 결과로 이동"""
#         if not self.search_results:
#             return
            
#         self.current_search_index = (self.current_search_index - 1) % len(self.search_results)
#         self.show_search_result(self.current_search_index)
#         self.search_info_label.config(
#             text=f"검색 결과: {len(self.search_results)}개 파일 "
#                  f"({self.current_search_index + 1}/{len(self.search_results)})")
                 
#     def next_search_result(self):
#         """다음 검색 결과로 이동"""
#         if not self.search_results:
#             return
            
#         self.current_search_index = (self.current_search_index + 1) % len(self.search_results)
#         self.show_search_result(self.current_search_index)
#         self.search_info_label.config(
#             text=f"검색 결과: {len(self.search_results)}개 파일 "
#                  f"({self.current_search_index + 1}/{len(self.search_results)})")
                 
#     def show_context_menu(self, event):
#         """파일 목록 우클릭 메뉴"""
#         menu = tk.Menu(self.root, tearoff=0)
#         menu.add_command(label="복사", command=self.copy_selected_file)
#         menu.post(event.x_root, event.y_root)
        
#     def copy_selected_file(self):
#         """선택된 파일명 복사"""
#         selection = self.file_listbox.curselection()
#         if selection:
#             file_text = self.file_listbox.get(selection[0])
#             file_name = file_text.split("📄 ")[1].split("  (")[0]
#             self.root.clipboard_clear()
#             self.root.clipboard_append(file_name)
            
#     def show_content_context_menu(self, event):
#         """파일 내용 우클릭 메뉴"""
#         menu = tk.Menu(self.root, tearoff=0)
        
#         if self.view_mode == "table":
#             menu.add_command(label="행 복사", command=self.copy_selected_row)
#             menu.add_command(label="셀 복사", command=self.copy_selected_cell)
#         else:
#             menu.add_command(label="선택 영역 복사", command=self.copy_selected_text)
#             menu.add_command(label="전체 복사", command=self.copy_all_text)
            
#         menu.post(event.x_root, event.y_root)
        
#     def copy_selected_row(self):
#         """선택된 행 복사"""
#         selection = self.content_tree.selection()
#         if selection:
#             item = selection[0]
#             values = self.content_tree.item(item)['values']
#             text = '\t'.join(str(v) for v in values)
#             self.root.clipboard_clear()
#             self.root.clipboard_append(text)
            
#     def copy_selected_cell(self):
#         """선택된 셀 복사"""
#         selection = self.content_tree.selection()
#         if selection:
#             item = selection[0]
#             col = self.content_tree.focus()
#             values = self.content_tree.item(item)['values']
#             if values:
#                 self.root.clipboard_clear()
#                 self.root.clipboard_append(str(values[0]))
                
#     def copy_selected_text(self):
#         """선택된 텍스트 복사"""
#         try:
#             selected_text = self.content_text.get(tk.SEL_FIRST, tk.SEL_LAST)
#             self.root.clipboard_clear()
#             self.root.clipboard_append(selected_text)
#         except:
#             pass
            
#     def copy_all_text(self):
#         """전체 텍스트 복사"""
#         text = self.content_text.get(1.0, tk.END)
#         self.root.clipboard_clear()
#         self.root.clipboard_append(text)


# def main():
#     root = tk.Tk()
#     app = ForensicFileViewer(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()

import os
import csv
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

HEX_BYTES_PER_LINE = 16

class ForensicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Forensic Viewer")
        self.geometry("1500x900")

        # state
        self.base_path = None
        self.search_index = {}
        self.current_bottom_path = None
        self.current_bottom_mode = None  # "csv","txt","hex"
        self.bottom_match_items = []
        self.hex_match_positions = []
        self.current_match_idx = -1

        self._build_ui()

    def _build_ui(self):
        # Top controls
        top = ttk.Frame(self)
        top.pack(fill="x", padx=6, pady=6)
        ttk.Button(top, text="폴더 선택", command=self.open_folder).pack(side="left")
        self.global_search_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.global_search_var, width=22).pack(side="left", padx=(8,4))
        ttk.Button(top, text="전체 검색", command=self.do_global_search).pack(side="left")

        # category bar
        self.cat_frame = ttk.Frame(self)
        self.cat_frame.pack(fill="x", padx=6, pady=(6,0))

        # main paned
        main_paned = ttk.Panedwindow(self, orient="horizontal")
        main_paned.pack(fill="both", expand=True, padx=6, pady=6)

        # left tree
        left_frame = ttk.Frame(main_paned)
        self.left_tree = ttk.Treeview(left_frame, show="tree")
        self.left_tree.grid(row=0, column=0, sticky="nsew")
        left_v = ttk.Scrollbar(left_frame, orient="vertical", command=self.left_tree.yview)
        left_v.grid(row=0, column=1, sticky="ns")
        self.left_tree.configure(yscrollcommand=left_v.set)
        left_frame.rowconfigure(0, weight=1); left_frame.columnconfigure(0, weight=1)
        self.left_tree.bind("<<TreeviewOpen>>", self._on_left_open)
        self.left_tree.bind("<<TreeviewSelect>>", self._on_left_select)
        main_paned.add(left_frame, weight=1)

        # right vertical (middle + bottom)
        right_paned = ttk.Panedwindow(main_paned, orient="vertical")
        main_paned.add(right_paned, weight=3)

        # middle frame
        middle_frame = ttk.Frame(right_paned)
        self.middle_table = ttk.Treeview(middle_frame, columns=("path","type","size","mtime"), show="headings")
        for col,w in (("path",400),("type",80),("size",100),("mtime",160)):
            self.middle_table.heading(col, text=col.capitalize(), command=lambda c=col: self._sort_middle_by(c))
            self.middle_table.column(col, width=w)
        self.middle_table.grid(row=0, column=0, sticky="nsew")
        mid_v = ttk.Scrollbar(middle_frame, orient="vertical", command=self.middle_table.yview)
        mid_v.grid(row=0, column=1, sticky="ns")
        self.middle_table.configure(yscrollcommand=mid_v.set)
        middle_frame.rowconfigure(0, weight=1); middle_frame.columnconfigure(0, weight=1)
        self.middle_table.bind("<<TreeviewSelect>>", self._on_middle_select)
        right_paned.add(middle_frame, weight=2)

        # bottom frame container
        bottom_frame = ttk.Frame(right_paned)

        # file internal search area
        nav = ttk.Frame(bottom_frame)
        nav.grid(row=0, column=0, sticky="ew", pady=(0,4))
        self.file_search_var = tk.StringVar()
        self.file_search_entry = ttk.Entry(nav, textvariable=self.file_search_var, width=30)
        self.file_search_entry.pack(side="left")
        ttk.Button(nav, text="찾기", command=self.do_file_search).pack(side="left", padx=(4,6))
        ttk.Button(nav, text="← Prev", command=self._file_prev).pack(side="right")
        ttk.Button(nav, text="Next →", command=self._file_next).pack(side="right", padx=(4,0))
        self.match_label = ttk.Label(nav, text="Matches: 0")
        self.match_label.pack(side="right", padx=(8,4))

        # content area: two separate frames (csv_frame and text_frame)
        content_container = ttk.Frame(bottom_frame)
        content_container.grid(row=1, column=0, sticky="nsew")
        bottom_frame.rowconfigure(1, weight=1); bottom_frame.columnconfigure(0, weight=1)

        # --- CSV frame with its own scrollbars ---
        self.csv_frame = ttk.Frame(content_container)
        self.csv_frame.grid(row=0, column=0, sticky="nsew")
        # vertical scrollbar
        self.csv_v = ttk.Scrollbar(self.csv_frame, orient="vertical")
        self.csv_v.grid(row=0, column=2, sticky="ns")
        # horizontal scrollbar
        self.csv_h = ttk.Scrollbar(self.csv_frame, orient="horizontal")
        self.csv_h.grid(row=1, column=0, columnspan=2, sticky="ew")
        # treeview for csv
        self.csv_table = ttk.Treeview(self.csv_frame, show="headings")
        self.csv_table.grid(row=0, column=0, sticky="nsew")
        self.csv_table.configure(yscrollcommand=self.csv_v.set, xscrollcommand=self.csv_h.set)
        self.csv_v.configure(command=self.csv_table.yview)
        self.csv_h.configure(command=self.csv_table.xview)
        self.csv_frame.rowconfigure(0, weight=1); self.csv_frame.columnconfigure(0, weight=1)

        # --- Text/Hex frame with its own scrollbars ---
        self.text_frame = ttk.Frame(content_container)
        self.text_frame.grid(row=0, column=0, sticky="nsew")  # occupies same grid cell; we'll raise/hide frames
        # vertical scrollbar
        self.txt_v = ttk.Scrollbar(self.text_frame, orient="vertical")
        self.txt_v.grid(row=0, column=1, sticky="ns")
        # horizontal scrollbar
        self.txt_h = ttk.Scrollbar(self.text_frame, orient="horizontal")
        self.txt_h.grid(row=1, column=0, sticky="ew")
        # text widget
        self.hex_text = tk.Text(self.text_frame, wrap="none", font=("Consolas",10))
        self.hex_text.grid(row=0, column=0, sticky="nsew")
        self.hex_text.configure(yscrollcommand=self.txt_v.set, xscrollcommand=self.txt_h.set)
        self.txt_v.configure(command=self.hex_text.yview)
        self.txt_h.configure(command=self.hex_text.xview)
        self.text_frame.rowconfigure(0, weight=1); self.text_frame.columnconfigure(0, weight=1)

        # initially hide both, will show one on demand
        self.csv_frame.grid_remove()
        self.text_frame.grid_remove()

        right_paned.add(bottom_frame, weight=3)

    # -------------------------
    # Left tree handlers
    # -------------------------
    def open_folder(self):
        folder = filedialog.askdirectory(title="분석 폴더 선택")
        if not folder:
            return
        self.base_path = folder
        self._render_categories()
        self.left_tree.delete(*self.left_tree.get_children())
        root_id = self.left_tree.insert("", "end", text=os.path.basename(folder) or folder, values=(folder,), open=True)
        self._populate_left_node(root_id, folder)
        self._clear_middle()
        self._clear_bottom()

    def _populate_left_node(self, parent_id, path):
        try:
            entries = sorted(os.listdir(path), key=str.lower)
        except Exception:
            return
        for name in entries:
            full = os.path.join(path, name)
            if os.path.isdir(full):
                nid = self.left_tree.insert(parent_id, "end", text=name, values=(full,))
                # add dummy for lazy expand
                self.left_tree.insert(nid, "end", text="(dummy)")
            else:
                self.left_tree.insert(parent_id, "end", text=name, values=(full,))

    def _on_left_open(self, event):
        item = self.left_tree.focus()
        if not item: return
        children = self.left_tree.get_children(item)
        if len(children) == 1 and self.left_tree.item(children[0], "text") == "(dummy)":
            self.left_tree.delete(children[0])
            path = self.left_tree.item(item, "values")[0]
            if os.path.isdir(path):
                self._populate_left_node(item, path)

    def _on_left_select(self, event):
        sel = self.left_tree.focus()
        if not sel: return
        path = self.left_tree.item(sel, "values")[0]
        if os.path.isdir(path):
            self._show_folder_in_middle(path)
        else:
            self._show_file_meta_in_middle(path)
        # do NOT change bottom view on left select
        self._clear_bottom()

    # -------------------------
    # Middle table
    # -------------------------
    def _render_categories(self):
        for w in self.cat_frame.winfo_children():
            w.destroy()
        if not self.base_path:
            return
        try:
            dirs = sorted(d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path,d)))
        except Exception:
            dirs = []
        for d in dirs:
            ttk.Button(self.cat_frame, text=d, command=lambda x=d: self._open_category(x)).pack(side="left", padx=3)
        for term in sorted(self.search_index.keys()):
            b = ttk.Button(self.cat_frame, text=term, command=lambda t=term: self._open_search_category(t))
            b.pack(side="left", padx=3)
            b.bind("<Button-3>", lambda e,t=term: self._delete_search_menu(e,t))

    def _delete_search_menu(self, event, term):
        m = tk.Menu(self, tearoff=0); m.add_command(label="삭제", command=lambda: self._delete_search_term(term)); m.tk_popup(event.x_root,event.y_root)

    def _delete_search_term(self, term):
        if term in self.search_index: del self.search_index[term]
        self._render_categories()

    def _open_category(self, name):
        path = os.path.join(self.base_path,name)
        if os.path.isdir(path):
            self._show_folder_in_middle(path)
        else:
            self._show_file_meta_in_middle(path)
        self._clear_bottom()

    def _open_search_category(self, term):
        self._clear_middle()
        self._clear_bottom()
        files = sorted(self.search_index.get(term,[]))
        for p in files:
            try:
                st = os.stat(p)
                size = self._human_readable(st.st_size)
                mtime = datetime.fromtimestamp(st.st_mtime).isoformat(sep=" ")
            except Exception:
                size=""; mtime=""
            self.middle_table.insert("", "end", values=(p, "File", size, mtime))

    def _clear_middle(self):
        self.middle_table.delete(*self.middle_table.get_children())

    def _show_folder_in_middle(self, folder):
        self._clear_middle()
        try:
            entries = sorted(os.listdir(folder), key=str.lower)
        except Exception:
            entries=[]
        for name in entries:
            full = os.path.join(folder, name)
            try:
                st = os.stat(full)
                size = self._human_readable(st.st_size) if os.path.isfile(full) else ""
                mtime = datetime.fromtimestamp(st.st_mtime).isoformat(sep=" ")
            except Exception:
                size=""; mtime=""
            typ = "Dir" if os.path.isdir(full) else "File"
            self.middle_table.insert("", "end", values=(full, typ, size, mtime), text=name)

    def _show_file_meta_in_middle(self, path):
        self._clear_middle()
        try:
            st = os.stat(path)
            size = self._human_readable(st.st_size)
            mtime = datetime.fromtimestamp(st.st_mtime).isoformat(sep=" ")
        except Exception:
            size=""; mtime=""
        self.middle_table.insert("", "end", values=(path, "File", size, mtime), text=os.path.basename(path))

    def _on_middle_select(self, event):
        sel = self.middle_table.focus()
        if not sel: return
        vals = self.middle_table.item(sel, "values")
        if not vals: return
        path = vals[0]
        if os.path.isdir(path):
            self._show_folder_in_middle(path)
            self._clear_bottom()
            return
        # show bottom content (explicitly triggered by middle selection)
        self._display_bottom_for_file(path)

    def _sort_middle_by(self, col):
        cols = list(self.middle_table["columns"])
        try:
            idx = cols.index(col)
        except ValueError:
            return
        items = list(self.middle_table.get_children())
        if not items: return
        def parse(v):
            try: return int(str(v).replace(" B","").replace(",",""))
            except: pass
            try: return datetime.fromisoformat(v)
            except: pass
            return str(v).lower()
        rev = getattr(self, "_mid_rev_"+col, False)
        sorted_items = sorted(items, key=lambda iid: parse(self.middle_table.item(iid,"values")[idx]), reverse=rev)
        for i,iid in enumerate(sorted_items):
            self.middle_table.move(iid,"",i)
        setattr(self, "_mid_rev_"+col, not rev)

    # -------------------------
    # Bottom display control
    # -------------------------
    def _clear_bottom(self):
        # csv frame hide
        self.csv_table_reset()
        self.csv_frame.grid_remove()
        # text frame hide
        self.hex_text.delete("1.0","end")
        self.text_frame.grid_remove()
        # clear match states
        self.bottom_match_items.clear()
        self.hex_match_positions.clear()
        self.current_match_idx = -1
        self.match_label.config(text="Matches: 0")
        self.current_bottom_path = None
        self.current_bottom_mode = None

    def csv_table_reset(self):
        try:
            self.csv_table.delete(*self.csv_table.get_children())
            self.csv_table["columns"] = ()
        except Exception:
            pass

    def _display_bottom_for_file(self, path):
        # show appropriate frame and load data
        self._clear_bottom()
        self.current_bottom_path = path
        low = path.lower()
        if low.endswith(".csv"):
            self._show_csv(path)
        elif low.endswith(".txt"):
            self._show_txt(path)
        else:
            self._show_hex(path)

    # CSV display
    def _show_csv(self, path):
        encodings = ("utf-8","cp949","latin1")
        headers = None
        used = None
        for enc in encodings:
            try:
                with open(path, encoding=enc, newline="") as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)
                    if headers is None:
                        headers = ["Column1"]
                    cols = ["Line"] + headers + ["Match"]
                    self.csv_table["columns"] = cols
                    # remove old headings first
                    for h in self.csv_table["columns"]:
                        self.csv_table.heading(h, text=h, command=lambda c=h: self._sort_csv_by(c))
                        # set width; allow xscroll
                        if h == "Line":
                            self.csv_table.column(h, width=70, anchor="center")
                        elif h == "Match":
                            self.csv_table.column(h, width=40, anchor="center", stretch=False)
                        else:
                            self.csv_table.column(h, width=180, anchor="w")
                    # insert rows streaming
                    line_no = 1
                    for row in reader:
                        if len(row) < len(headers):
                            row = row + [""]*(len(headers)-len(row))
                        elif len(row) > len(headers):
                            row = row[:len(headers)]
                        self.csv_table.insert("", "end", values=[line_no] + row + [""])
                        line_no += 1
                used = enc
                break
            except Exception:
                continue
        if used is None:
            # fallback to hex
            self._show_hex(path)
            return
        # configure tags
        self.csv_table.tag_configure("match", background="#fff176")
        self.csv_table.tag_configure("normal", background="white")
        # show csv frame and ensure its scrollbars work
        self.csv_frame.grid()
        self.current_bottom_mode = "csv"
        self.match_label.config(text="Matches: 0")

    # TXT display (text frame)
    def _show_txt(self, path):
        encodings = ("utf-8","cp949","latin1")
        used = None
        self.text_frame.grid()
        for enc in encodings:
            try:
                with open(path, encoding=enc, errors="replace") as f:
                    for i,line in enumerate(f, start=1):
                        self.hex_text.insert("end", f"{i:06d}: {line}")
                used = enc
                break
            except Exception:
                continue
        if used is None:
            self.hex_text.insert("end", "텍스트 파일 읽기 실패(인코딩 문제)\n")
        self.current_bottom_mode = "txt"
        self.match_label.config(text="Matches: 0")

    # HEX display (text frame)
    def _show_hex(self, path):
        self.text_frame.grid()
        try:
            with open(path, "rb") as f:
                off = 0
                while True:
                    chunk = f.read(HEX_BYTES_PER_LINE)
                    if not chunk:
                        break
                    hexpart = " ".join(f"{b:02X}" for b in chunk)
                    asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
                    line = f"{off:08X}  {hexpart:<{HEX_BYTES_PER_LINE*3}}  {asc}\n"
                    self.hex_text.insert("end", line)
                    off += HEX_BYTES_PER_LINE
        except Exception as e:
            self.hex_text.insert("end", f"HEX 읽기 오류: {e}\n")
        self.current_bottom_mode = "hex"
        self.match_label.config(text="Matches: 0")

    def _sort_csv_by(self, col):
        cols = list(self.csv_table["columns"])
        try:
            idx = cols.index(col)
        except ValueError:
            return
        items = list(self.csv_table.get_children())
        if not items:
            return
        def parse(v):
            try: return int(v)
            except: pass
            try: return float(v)
            except: pass
            try: return datetime.fromisoformat(v)
            except: pass
            return str(v).lower()
        rev = getattr(self, "_csv_rev_"+col, False)
        sorted_items = sorted(items, key=lambda iid: parse(self.csv_table.item(iid,"values")[idx] if idx < len(self.csv_table.item(iid,"values")) else ""), reverse=rev)
        for i,iid in enumerate(sorted_items):
            self.csv_table.move(iid, "", i)
        setattr(self, "_csv_rev_"+col, not rev)

    # -------------------------
    # File-internal search
    # -------------------------
    def do_file_search(self):
        q = self.file_search_var.get().strip()
        # clear search input per requirement
        self.file_search_var.set("")
        if not q or not self.current_bottom_path:
            return
        # clear previous
        self._clear_highlight()
        patt = re.compile(re.escape(q), re.IGNORECASE)
        if self.current_bottom_mode == "csv":
            for iid in self.csv_table.get_children():
                vals = self.csv_table.item(iid, "values")
                row_text = " ".join(str(v) for v in vals)
                if patt.search(row_text):
                    self.csv_table.item(iid, tags=("match",))
                    self.bottom_match_items.append(iid)
                else:
                    self.csv_table.item(iid, tags=("normal",))
            cnt = len(self.bottom_match_items)
            self.match_label.config(text=f"Matches: {cnt}")
            if cnt:
                self.current_match_idx = 0
                self._select_csv_match(0)
        else:
            # text or hex view: search text widget
            self._search_in_text_widget(patt)

    def _search_in_text_widget(self, patt):
        t = self.hex_text
        t.tag_remove("hl", "1.0", "end")
        self.hex_match_positions.clear()
        start = "1.0"
        while True:
            idx = t.search(patt, start, stopindex="end", nocase=True)
            if not idx:
                break
            line_start = idx.split(".")[0] + ".0"
            t.tag_add("hl", line_start, f"{line_start} lineend")
            self.hex_match_positions.append(line_start)
            start = f"{idx} + 1 chars"
        t.tag_config("hl", background="#fff176")
        cnt = len(self.hex_match_positions)
        self.match_label.config(text=f"Matches: {cnt}")
        if cnt:
            self.current_match_idx = 0
            self._select_text_match(0)

    def _clear_highlight(self):
        for iid in self.csv_table.get_children():
            self.csv_table.item(iid, tags=("normal",))
        self.csv_table.tag_configure("normal", background="white")
        self.hex_text.tag_remove("hl", "1.0", "end")
        self.bottom_match_items.clear()
        self.hex_match_positions.clear()
        self.current_match_idx = -1
        self.match_label.config(text="Matches: 0")

    def _select_csv_match(self, idx):
        if not self.bottom_match_items:
            return
        iid = self.bottom_match_items[idx]
        self.csv_table.selection_set(iid)
        self.csv_table.see(iid)
        self.current_match_idx = idx
        self.match_label.config(text=f"Matches: {len(self.bottom_match_items)} ({idx+1}/{len(self.bottom_match_items)})")

    def _select_text_match(self, idx):
        if not self.hex_match_positions:
            return
        pos = self.hex_match_positions[idx]
        self.hex_text.see(pos)
        self.current_match_idx = idx
        self.match_label.config(text=f"Matches: {len(self.hex_match_positions)} ({idx+1}/{len(self.hex_match_positions)})")

    def _file_prev(self):
        if self.current_bottom_mode == "csv" and self.bottom_match_items:
            idx = (self.current_match_idx - 1) % len(self.bottom_match_items)
            self._select_csv_match(idx)
        elif self.hex_match_positions:
            idx = (self.current_match_idx - 1) % len(self.hex_match_positions)
            self._select_text_match(idx)

    def _file_next(self):
        if self.current_bottom_mode == "csv" and self.bottom_match_items:
            idx = (self.current_match_idx + 1) % len(self.bottom_match_items)
            self._select_csv_match(idx)
        elif self.hex_match_positions:
            idx = (self.current_match_idx + 1) % len(self.hex_match_positions)
            self._select_text_match(idx)

    # -------------------------
    # Global search (create category)
    # -------------------------
    def do_global_search(self):
        term = self.global_search_var.get().strip()
        if not term or not self.base_path:
            return
        patt = re.compile(re.escape(term), re.IGNORECASE)
        matches = set()
        for root, dirs, files in os.walk(self.base_path):
            for fn in files:
                full = os.path.join(root, fn)
                if self._file_contains(full, patt):
                    matches.add(full)
        if matches:
            self.search_index[term] = sorted(matches)
            self._render_categories()
        self.global_search_var.set("")

    def _file_contains(self, path, patt):
        try:
            with open(path, "rb") as f:
                while True:
                    chunk = f.read(65536)
                    if not chunk:
                        break
                    txt = chunk.decode("latin1", errors="ignore")
                    if patt.search(txt):
                        return True
            return False
        except Exception:
            return False

    # utilities
    def _human_readable(self, n):
        for unit in ["B","KB","MB","GB","TB"]:
            if n < 1024:
                return f"{int(n)} {unit}"
            n = n/1024
        return f"{n:.1f} PB"

if __name__ == "__main__":
    app = ForensicApp()
    app.mainloop()
