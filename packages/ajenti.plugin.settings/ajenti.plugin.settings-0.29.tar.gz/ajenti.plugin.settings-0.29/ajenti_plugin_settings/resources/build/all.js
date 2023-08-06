'use strict';

angular.module('ajenti.settings', ['core', 'ajenti.filesystem', 'ajenti.passwd']);

angular.module('ajenti.settings').run(function (customization) {
    return customization.plugins.settings = {};
});


'use strict';

angular.module('core').config(function ($routeProvider) {
    return $routeProvider.when('/view/settings', {
        templateUrl: '/settings:resources/partial/index.html',
        controller: 'SettingsIndexController'
    });
});


'use strict';

angular.module('ajenti.settings').controller('SettingsIndexController', function ($scope, $http, $sce, notify, pageTitle, identity, messagebox, passwd, config, core, locale, gettext) {
    pageTitle.set(gettext('Settings'));

    $scope.config = config;
    $scope.oldCertificate = config.data.ssl.certificate;

    $scope.availableColors = ['default', 'bluegrey', 'red', 'deeporange', 'orange', 'green', 'teal', 'blue', 'purple'];

    $scope.newClientCertificate = {
        c: 'NA',
        st: 'NA',
        o: '',
        cn: ''
    };

    identity.promise.then(function () {
        $scope.newClientCertificate.o = identity.machine.name;
        passwd.list().then(function (data) {
            $scope.availableUsers = data;
            $scope.$watch('newClientCertificate.user', function () {
                return $scope.newClientCertificate.cn = identity.user + '@' + identity.machine.hostname;
            });
            $scope.newClientCertificate.user = 'root';
        });
        $http.get('/api/core/languages').then(function (rq) {
            return $scope.languages = rq.data;
        });
    });

    config.load().then(function () {
        return config.getAuthenticationProviders(config);
    }, function () {
        return notify.error(gettext('Could not load config'));
    }).then(function (p) {
        return $scope.authenticationProviders = p;
    }).catch(function () {
        return notify.error(gettext('Could not load authentication provider list'));
    });

    $scope.$watch('config.data.color', function () {
        if (config.data) {
            identity.color = config.data.color;
        }
    });

    $scope.$watch('config.data.language', function () {
        if (config.data) {
            locale.setLanguage(config.data.language);
        }
    });

    $scope.save = function () {
        $scope.certificate = config.data.ssl.certificate;
        if ($scope.certificate != $scope.oldCertificate) {
            return $http.post('/api/settings/test-certificate/', { 'certificate': $scope.certificate }).then(function (data) {
                config.save().then(function (dt) {
                    return notify.success(gettext('Saved'));
                });
            }).catch(function (err) {
                notify.error(gettext('SSL Error')), err.message;
            });
        } else {
            config.save().then(function (data) {
                return notify.success(gettext('Saved'));
            }).catch(function () {
                return notify.error(gettext('Could not save config'));
            });
        }
    };

    $scope.createNewServerCertificate = function () {
        return messagebox.show({
            title: gettext('Self-signed certificate'),
            text: gettext('Generating a new certificate will void all existing client authentication certificates!'),
            positive: gettext('Generate'),
            negative: gettext('Cancel')
        }).then(function () {
            config.data.ssl.client_auth.force = false;
            notify.info(gettext('Generating certificate'), gettext('Please wait'));
            return $http.get('/api/settings/generate-server-certificate').success(function (data) {
                notify.success(gettext('Certificate successfully generated'));
                config.data.ssl.enable = true;
                config.data.ssl.certificate = data.path;
                config.data.ssl.client_auth.certificates = [];
                $scope.save();
            }).error(function (err) {
                return notify.error(gettext('Certificate generation failed'), err.message);
            });
        });
    };

    $scope.generateClientCertificate = function () {
        $scope.newClientCertificate.generating = true;
        return $http.post('/api/settings/generate-client-certificate', $scope.newClientCertificate).success(function (data) {
            $scope.newClientCertificate.generating = false;
            $scope.newClientCertificate.generated = true;
            $scope.newClientCertificate.url = $sce.trustAsUrl('data:application/x-pkcs12;base64,' + data.b64certificate);
            config.data.ssl.client_auth.certificates.push({
                user: $scope.newClientCertificate.user,
                digest: data.digest,
                name: data.name,
                serial: data.serial
            });
        }).error(function (err) {
            $scope.newClientCertificate.generating = false;
            $scope.newClientCertificateDialogVisible = false;
            notify.error(gettext('Certificate generation failed'), err.message);
        });
    };

    $scope.addEmail = function (email, username) {
        config.data.auth.emails[email] = username;
        $scope.newEmailDialogVisible = false;
    };

    $scope.removeEmail = function (email) {
        return delete config.data.auth.emails[email];
    };

    $scope.restart = function () {
        return core.restart();
    };
});


