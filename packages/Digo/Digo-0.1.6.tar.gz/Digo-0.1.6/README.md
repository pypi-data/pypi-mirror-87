#Start to Digo
Digo.init(api_key="API-KEY", project_name="project", workspace_name="workspace")

#Send Parameter
Digo.setParameter(parser)

#Send Log
Digo.log({'loss':loss, 'mIou':mIou})

#Send Image Data 
Digo.imageLog({'input':_input,'groud':_ground,'output':_output})

#Save Model File
Digo.uploadModel('model.pth')