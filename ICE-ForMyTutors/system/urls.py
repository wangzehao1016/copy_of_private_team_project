from django.urls import path
from . import views
from .moreviews import manageModules,studyModule

urlpatterns = [
    # both users
    path('view/<int:user_id>/', views.showCourses, name='showCourses'),                                               # view course list
    path('view/<int:user_id>/<int:course_id>/', views.showModules, name='showModules'),                               # view module list
    path('view/<int:user_id>/<int:course_id>/<int:module_id>/', studyModule.viewModule, name='viewModule'),      # view component list
    #path('view/<int:user_id>/<int:course_id>/<int:module_id>/', views.showComponents, name='showComponents'),          # view component list

    # instructor editing mode
    path('manage/<int:instructor_id>/<int:course_id>/requestAdd/', views.enterModuleInfo, name='enterModuleInfo'),
    path('manage/<int:instructor_id>/<int:course_id>/add/',views.addModule, name='manageModule'),
    path('manage/<int:instructor_id>/<int:course_id>/<int:module_id>/deleteModule/', views.deleteModule, name="deleteModule"),
    path('manage/<int:instructor_id>/<int:course_id>/<int:module_id>/selectQuiz/', views.showQuizzes, name='showQuizzes'),    # add quiz view
    path('manage/<int:instructor_id>/<int:course_id>/<int:module_id>/addQuiz/<int:quiz_id>/', views.addQuiz, name="addQuiz"),
    path('manage/<int:instructor_id>/<int:course_id>/<int:module_id>/<int:quiz_id>/removeQuiz/', views.removeQuiz, name="removeQuiz"),
    path('manage/<int:instructor_id>/<int:course_id>/<int:module_id>/addComponent/',manageModules.selectComponent, name='display_available_components'),
    path('manage/<int:instructor_id>/<int:course_id>/<int:module_id>/addComponent/<int:component_id>/',manageModules.addComponent, name='append_component'),
    path('manage/<int:instructor_id>/<int:course_id>/<int:module_id>/displayModuleContent/',manageModules.displayModuleContent,name='displayModuleContent'),
    path('manage/<int:instructor_id>/<int:course_id>/<int:module_id>/saveOrder/<slug:neworder>/',manageModules.saveOrder,name='saveOrder'),
    path('manage/<int:instructor_id>/<int:course_id>/<int:module_id>/removeComponent/<int:component_id>',manageModules.removeComponent,name='removeComponentFromModule'),

    # learner study mode
    # path('view/<int:user_id>/', studyModule.viewEnrolled, name='viewEnrolled'),   # view course list
    # path('view/<int:user_id>/<int:course_id>/', views.viewCourse, name='viewCourse'),                           # view module list

    path('view/<int:user_id>/<int:course_id>/<int:module_id>/quiz/', studyModule.takeQuiz, name='takeQuiz'),        # learner takes quiz
    path('view/<int:user_id>/<int:course_id>/<int:module_id>/quiz/submitAnswer/', studyModule.submitAnswer, name='submitAnswer'),        # learner submits answer

]
